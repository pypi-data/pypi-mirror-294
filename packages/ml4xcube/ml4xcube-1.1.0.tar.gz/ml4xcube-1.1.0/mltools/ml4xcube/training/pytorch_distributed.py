import os
import torch
import torch.distributed as dist
from typing import Dict, Callable
from torch.utils.data import DataLoader
from ml4xcube.training.train_plots import plot_loss
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed.elastic.multiprocessing.errors import record
from torch.distributed import init_process_group, destroy_process_group


def ddp_init() -> None:
    """
    Initializes the distributed process group.
    Uses NCCL (NVIDIA Collective Communications Library) as the backend for GPU-based distributed training.
    Sets the current device based on the worker's local rank environment variable.
    """
    init_process_group(backend="nccl")
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))


class Trainer:
    """
    A trainer class for distributed training of PyTorch models.

    Supports supervised and unsupervised (reconstruction) tasks, early stopping,
    and periodic snapshot saving.
    """
    def __init__(
        self, model: torch.nn.Module, train_data: DataLoader, test_data: DataLoader,
        optimizer: torch.optim.Optimizer, model_path: str, save_every: int = 10,
        snapshot_path: str = None, early_stopping: bool = True, patience: int = 10,
        loss: Callable = None, metrics: Dict[str, Callable] = None, epochs: int = 10,
        validate_parallelism: bool = False, create_loss_plot: bool = False
    ):
        """
        Initialize the Trainer for distributed training.

        Args:
            model (torch.nn.Module): The PyTorch model to train.
            train_data (DataLoader): DataLoader for the training data.
            test_data (DataLoader): DataLoader for the validation/test data.
            optimizer (torch.optim.Optimizer): Optimizer for training.
            model_path (str): Path to save the best model.
            save_every (int): Frequency of saving training snapshots (in epochs).
            snapshot_path (str): Path to save training snapshots. Defaults to None.
            early_stopping (bool): Enable or disable early stopping. Defaults to True.
            patience (int,): Number of epochs to wait for improvement before stopping early. Defaults to 10.
            loss (Callable): Loss function. Defaults to None.
            metrics (Dict[str, Callable]): Dictionary of metrics to evaluate during validation, with metric
                                                     names as keys and metric functions as values. Defaults to None.
            epochs (int): Number of epochs to train the model. Defaults to 10.
            validate_parallelism (bool): If set to True, prints loss information from each GPU, useful for
                                                   debugging and performance tuning. Defaults to False.
            create_loss_plot (bool): Whether to create a plot of training and validation loss after training.
                                               Defaults to False.

        Attributes:
            gpu_id (int): The ID of the GPU assigned to the current process, derived from the `LOCAL_RANK` environment variable.
            ddp_model (torch.nn.Module): The PyTorch model wrapped with DistributedDataParallel (DDP) for multi-GPU training.
            epochs_run (int): The number of epochs that have been run. Used to resume training from a checkpoint.
            best_val_loss (float): The best validation loss encountered during training, initialized to infinity.
            strikes (int): A counter tracking the number of consecutive epochs without validation loss improvement.
            train_list (List[float]): A list to store the average training loss for each epoch.
            val_list (List[float]): A list to store the average validation loss for each epoch.
        """
        self.gpu_id = int(os.environ["LOCAL_RANK"])  # GPU ID for the current process
        self.model = model.to(self.gpu_id)  # Moves model to the correct device
        self.train_data = train_data
        self.test_data = test_data
        self.optimizer = optimizer
        self.save_every = save_every  # Frequency of saving training snapshots
        self.epochs_run = 0  # Tracks the number of epochs run
        self.model_path = model_path # Path to best model computed in current training
        self.snapshot_path = snapshot_path  # Path to save snapshots
        self.early_stopping = early_stopping  # Enables/disables early stopping
        self.patience = patience  # Number of epochs to wait before early stop if no progress on the validation set
        self.best_val_loss = float('inf')  # Best validation loss for early stopping
        self.strikes = 0  # Counter for epochs without improvement
        self.loss = loss # Loss function
        self.metrics = metrics # Dict of metrics to compute for validation purposes
        self.epochs = epochs
        self.ddp_model = DDP(self.model, device_ids=[self.gpu_id], find_unused_parameters=True)  # Wraps the model for DDP
        self.validate_parallelism = validate_parallelism
        self.create_loss_plot = create_loss_plot
        self.train_list = list()
        self.val_list = list()

    def _load_snapshot(self, snapshot_path: str) -> None:
        """
        Loads a training snapshot to resume training.

        Args:
            snapshot_path (str): The path to the training snapshot file.
        """
        loc = f"cuda:{self.gpu_id}"
        snapshot = torch.load(snapshot_path, map_location=loc)
        self.model.load_state_dict(snapshot["MODEL_STATE"])
        self.epochs_run = snapshot["EPOCHS_RUN"]
        print(f"Resuming training from snapshot at Epoch {self.epochs_run + 1}")

    def _run_batch(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Runs a single batch of training data through the model.

        Args:
            inputs (torch.Tensor): Input data for the model.
            targets (torch.Tensor): Target data for the training.

        Returns:
            torch.Tensor: The loss value for the batch.
        """
        inputs, targets = inputs.to(self.gpu_id), targets.to(self.gpu_id)
        self.optimizer.zero_grad()
        outputs = self.ddp_model(inputs)
        loss = self.loss(outputs, targets)
        loss.backward()

        if self.validate_parallelism:  # Check if loss printing is enabled
            # Print loss for the current GPU along with the processing time of the batch
            print(f"GPU {self.gpu_id} | Batch Loss: {loss.item():.4f}")
        return loss

    def _run_epoch(self, epoch: int) -> None:
        """
        Runs a single epoch of training.

        Args:
            epoch (int): The current epoch number.
        """
        running_loss = 0.0
        running_size = 0
        self.train_data.sampler.set_epoch(epoch)
        for inputs, targets in self.train_data:
            with torch.set_grad_enabled(True):
                if inputs.numel() == 0: continue
                loss = self._run_batch(inputs, targets)
            running_loss += loss.item() * len(inputs)
            running_size += len(inputs)

        avg_epoch_loss = running_loss / running_size
        self.train_list.append(avg_epoch_loss)
        if self.gpu_id == 0:
            print(f"Epoch {epoch + 1} | Average Loss: {avg_epoch_loss:.4f}")

    def _validate(self) -> float:
        """
        Validates the model on the test dataset.

        Returns:
            float: The average validation loss across all test data.
        """
        self.ddp_model.eval()  # Set the model to evaluation mode
        running_loss = 0.0
        running_size = 0
        metric_sums = {}
        if self.metrics is not None:
            metric_sums = {name: 0.0 for name in self.metrics.keys()}
        for inputs, targets in self.test_data:
            with torch.no_grad():  # No need to track gradients during validation
                if inputs.numel() == 0: continue
                inputs, targets = inputs.to(self.gpu_id), targets.to(self.gpu_id)
                outputs = self.ddp_model(inputs)
                loss = self.loss(outputs, targets)
                running_loss += loss.item() * len(inputs)
                running_size += len(inputs)

                if self.metrics is not None:
                    for name, metric in self.metrics.items():
                        metric_value = metric(outputs, targets).item()
                        metric_sums[name] += metric_value * len(inputs)

        # Convert running loss and size to tensors for all_reduce operation
        running_loss_tensor = torch.tensor([running_loss], device=self.gpu_id)
        running_size_tensor = torch.tensor([running_size], device=self.gpu_id)

        if self.metrics is not None:
            running_metrics_tensors = {
                name: torch.tensor([metric_sum], device=self.gpu_id)
                for name, metric_sum in metric_sums.items()
            }

        dist.barrier()

        # Use dist.all_reduce to sum the losses and sizes from all GPUs
        dist.all_reduce(running_loss_tensor, op=dist.ReduceOp.SUM)
        dist.all_reduce(running_size_tensor, op=dist.ReduceOp.SUM)

        # Compute the average loss across all GPUs and samples
        avg_val_loss = running_loss_tensor.item() / running_size_tensor.item()

        # Compute average metrics across all GPUs
        if self.metrics is not None:
            for name, tensor in running_metrics_tensors.items():
                dist.all_reduce(tensor, op=dist.ReduceOp.SUM)

            avg_metrics = {
                name: (metric_sum.item() / running_size_tensor.item())
                for name, metric_sum in running_metrics_tensors.items()
            }

        self.val_list.append(avg_val_loss)

        if self.gpu_id == 0:
            print(f"Validation Loss: {avg_val_loss:.4e}")
            if self.metrics is not None:
                for name, value in avg_metrics.items():
                    print(f"{name}: {value:.4e}")
        return avg_val_loss

    def _save_snapshot(self, epoch: int) -> None:
        """
        Saves a training snapshot.

        Args:
            epoch (int): The current epoch number, for tracking in the snapshot.
        """
        snapshot = {
            "MODEL_STATE": self.ddp_model.module.state_dict(),
            "EPOCHS_RUN": epoch,
        }
        torch.save(snapshot, self.snapshot_path)
        print(f"Epoch {epoch + 1} | Training snapshot saved at {self.snapshot_path}")

    @record
    def train(self) -> torch.nn.Module:
        """
        The main training loop.

        Returns:
            torch.nn.Module: The model with the best weights loaded.
        """
        for epoch in range(self.epochs_run, self.epochs):
            self._run_epoch(epoch)
            if self.gpu_id == 0 and epoch % self.save_every == 0 and self.snapshot_path is not None:
                self._save_snapshot(epoch)
            dist.barrier()

            epoch_val_loss = self._validate()

            # Early Stopping Logic
            if epoch_val_loss < self.best_val_loss:
                self.strikes = 0
                self.best_val_loss = epoch_val_loss
                # Saving the best ddp_model
                torch.save(self.ddp_model.module.state_dict(), self.model_path)
                if self.gpu_id == 0:
                    print(f"New best model saved with validation loss: {epoch_val_loss}")
            else:
                self.strikes += 1

            if self.early_stopping:
                if self.strikes > self.patience:
                    if self.gpu_id == 0:
                        print('Stopping early due to no improvement.')
                    break

        destroy_process_group()
        
        if self.create_loss_plot:
            plot_loss(self.train_list, self.val_list)

        # Load the best weights from model_path into self.model
        loc = f"cuda:{0}"
        self.model.load_state_dict(torch.load(self.model_path, map_location=loc))

        print("Best model loaded.")

        return self.model






