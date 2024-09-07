import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import builtins

class SlackLogger:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel
        self.client = WebClient(token=self.token)

    def send_message(self, text):
        """Sends a message to the specified Slack channel."""
        try:
            response = self.client.chat_postMessage(channel=self.channel, text=text)
            if not response.get("ok"):
                print(f"Failed to send message: {response}")
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

    class SlackLoggerHandler(logging.Handler):
        def __init__(self, slack_logger):
            super().__init__()
            self.slack_logger = slack_logger

        def emit(self, record):
            log_entry = self.format(record)
            self.slack_logger.send_message(log_entry)

    @staticmethod
    def redirect_print_to_logger(logger):
        """Redirects print statements to the specified logger."""
        def print_to_logger(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)
            logger.info(message)
        builtins.print = print_to_logger

    @classmethod
    def read_slack_token(cls, aic_instance):
        """Reads the Slack token from the storage drive."""
        try:
            content = aic_instance.download_file(aic_instance.drive_id, 'slack_token.txt')
            if content:
                return content.strip()
            else:
                raise ValueError("Slack token file is empty or not found.")
        except Exception as e:
            print(f"Error reading Slack token: {str(e)}")
            raise ValueError("Failed to read Slack token from storage.")


    @classmethod
    def create_logger(cls, aic_instance=None, slack_token=None, slack_channel='C07DYFK5SE8', redirect_print=True):
        """Creates a logger that sends log messages to a Slack channel.

        Args:
            aic_instance: Instance of AIC for accessing the storage drive.
            slack_token (str): The Slack API token for authentication. If not provided, it will be read from the storage drive.
            slack_channel (str): The Slack channel ID to send messages to.
            redirect_print (bool): Whether to redirect print statements to the logger.

        Returns:
            logging.Logger: Configured logger instance with Slack handler.
        """
        # Retrieve the Slack token from the storage drive if not provided
        if not slack_token:
            slack_token = cls.read_slack_token(aic_instance)

        # Initialize SlackLogger and SlackLoggerHandler
        slack_logger = cls(slack_token, slack_channel)
        slack_handler = cls.SlackLoggerHandler(slack_logger)

        # Create a logger and attach the custom Slack handler
        logger = logging.getLogger('SlackLogger')
        logger.setLevel(logging.INFO)  # Set the logging level
        logger.addHandler(slack_handler)

        # Set a basic format for the log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        slack_handler.setFormatter(formatter)

        # Automatically redirect print statements if specified
        if redirect_print:
            cls.redirect_print_to_logger(logger)

        return logger