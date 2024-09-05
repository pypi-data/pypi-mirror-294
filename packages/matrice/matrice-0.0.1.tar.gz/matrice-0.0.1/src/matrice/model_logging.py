"""Module for handling logging of model training epochs in projects."""
import matplotlib.pyplot as plt
import seaborn as sns

class ModelLogging:
    """Class for managing model logging."""

    def __init__(self, session, model_id=None):
        """
        Initialize ModelLogging instance.

        Parameters
        ----------
        session : object
            The session object used to make RPC calls.
        model_id : str, optional
            The ID of the model to fetch logs for. Default is None.
        """
        self.model_id = model_id
        self.rpc = session.rpc

    def get_model_training_logs(self):
        """
        Get training logs for the specified model.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the RPC call.
            - An error message if the request fails.
            - A success message if the request is successful.

        Example
        -------
        >>> response, error, message = model_logging.get_model_training_logs()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Success: {message}")
        """
        path = f"/v1/model_logging/model/{self.model_id}/train_epoch_logs"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            error = None
            message = "Got all the models inside the project"
        else:
            error = resp.get("message")
            message = "Could not fetch model logs inside the project"

        return resp, error, message
    
    def plot_epochs_losses(self):
        """
        Plot training and validation losses over epochs.

        This method retrieves model training logs and generates two subplots:
        one for training losses and one for validation losses, displaying them
        over the epochs.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_losses()
        """
        resp, error, message = self.get_model_training_logs()
        training_logs = resp['data']

        epochs = []
        metrics = {
            'train': {},
            'val': {}
        }
        for epoch_data in training_logs:
            epochs.append(epoch_data['epoch'])
            for detail in epoch_data['epochDetails']:
                metric_name = detail['metricName']
                metric_value = detail['metricValue']
                split_type = detail['splitType']

                if "loss" in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)
        # Set plot style
        sns.set(style="whitegrid")
        # Plotting
        fig, axs = plt.subplots(2, 1, figsize=(12, 18))
        # Plot for train metrics
        for split_type, split_metrics in metrics.items():
            for metric_name in split_metrics.keys():
                if split_type == "train":
                    axs[0].plot(epochs, split_metrics[metric_name], label=f'{split_type} {metric_name}')
                elif split_type == "val":
                    axs[1].plot(epochs, split_metrics[metric_name], label=f'{split_type} {metric_name}')

        axs[0].set_xlabel('Epoch', fontsize=14)
        axs[0].set_ylabel('Loss', fontsize=14)
        axs[0].legend(fontsize=12)
        axs[0].set_title('Training Losses over Epochs', fontsize=16)
        axs[0].grid(True)

        axs[1].set_xlabel('Epoch', fontsize=14)
        axs[1].set_ylabel('Loss', fontsize=14)
        axs[1].legend(fontsize=12)
        axs[1].set_title('Validation Losses over Epochs', fontsize=16)
        axs[1].grid(True)
        plt.tight_layout()
        plt.show()
    
    def plot_epochs_metrics(self):
        """
        Plot training and validation metrics (excluding loss) over epochs.

        This method retrieves model training logs and generates subplots for each
        metric (excluding losses) over the epochs.

        Returns
        -------
        None

        Example
        -------
        >>> model_logging.plot_epochs_metrics()
        """
        resp, error, message = self.get_model_training_logs()
        training_logs = resp['data']
        epochs = []
        metrics = {
            'train': {},
            'val': {}
        }
        metrics_names = set()
        for epoch_data in training_logs:
            epochs.append(epoch_data['epoch'])
            for detail in epoch_data['epochDetails']:
                metric_name = detail['metricName']
                metric_value = detail['metricValue']
                split_type = detail['splitType']

                if "loss" not in metric_name:
                    if split_type not in metrics:
                        metrics[split_type] = []
                    if metric_name not in metrics[split_type]:
                        metrics[split_type][metric_name] = []
                    metrics[split_type][metric_name].append(metric_value)
                    metrics_names.add(metric_name)
        
        metrics_names = list(metrics_names)
        num_graphs = len(metrics_names)
        # Set plot style
        sns.set(style="whitegrid")
        # Plotting
        fig, axs = plt.subplots(num_graphs, 1, figsize=(12, 18))

        for metric_index in range(len(metrics_names)):
            metric_name = metrics_names[metric_index]
            for split_type, split_metrics in metrics.items():
                if metric_name in metrics[split_type]:
                    axs[metric_index].plot(epochs, split_metrics[metric_name], label=f'{split_type} {metric_name}')

            axs[metric_index].set_xlabel('Epoch', fontsize=14)
            axs[metric_index].set_ylabel(metric_name, fontsize=14)
            axs[metric_index].legend(fontsize=12)
            axs[metric_index].set_title(f'{metric_name} over Epochs', fontsize=16)
            axs[metric_index].grid(True)
        plt.tight_layout()
        plt.show()

