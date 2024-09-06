import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import builtins

class SlackLogger:
    def __init__(self, slack_token, slack_channel, redirect_print=True):
        """
        Initializes the SlackLogger with a Slack bot and channel, and optionally redirects print statements to the logger.

        Args:
            slack_token (str): Slack API token for authentication.
            slack_channel (str): Slack channel ID where messages will be sent.
            redirect_print (bool): Whether to redirect print statements to the Slack logger.
        """
        self.slack_bot = self.SlackBot(slack_token)
        self.slack_handler = self.SlackLoggerHandler(self.slack_bot, slack_channel)
        self.logger = self._setup_logger()

        # Automatically redirect print statements if specified
        if redirect_print:
            self.redirect_print_to_logger()

    class SlackBot:
        def __init__(self, token):
            self.client = WebClient(token=token)

        def send_message(self, channel, text):
            try:
                response = self.client.chat_postMessage(
                    channel=channel,
                    text=text
                )
                if response.get("ok"):
                    print("Message sent successfully!")
                else:
                    print(f"Failed to send message: {response}")
            except SlackApiError as e:
                print(f"Error sending message: {e.response['error']}")

    class SlackLoggerHandler(logging.Handler):
        def __init__(self, slack_bot, channel):
            super().__init__()
            self.slack_bot = slack_bot
            self.channel = channel

        def emit(self, record):
            log_entry = self.format(record)
            self.slack_bot.send_message(self.channel, log_entry)

    def _setup_logger(self):
        """
        Sets up the logger with a custom Slack handler and basic formatting.

        Returns:
            logger (logging.Logger): Configured logger with Slack handler.
        """
        logger = logging.getLogger('SlackLogger')
        logger.setLevel(logging.INFO)  # Set the logging level
        logger.addHandler(self.slack_handler)

        # Set a basic format for the log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.slack_handler.setFormatter(formatter)

        return logger

    def redirect_print_to_logger(self):
        """
        Redirects print statements to the Slack logger.
        """
        def print_to_logger(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)
            self.logger.info(message)

        # Override the built-in print function
        builtins.print = print_to_logger

    @classmethod
    def create_logger(cls, slack_token='xoxb-7424459969442-7456034210037-EMCjbI9oi1xTszU1iUh4tLFH', slack_channel='C07DYFK5SE8', redirect_print=True):
        """
        Creates and returns a Slack logger in a single line.

        Args:
            slack_token (str): Slack API token for authentication.
            slack_channel (str): Slack channel ID where messages will be sent.
            redirect_print (bool): Whether to redirect print statements to the Slack logger.

        Returns:
            logger (logging.Logger): Configured Slack logger instance.
        """
        instance = cls(slack_token, slack_channel, redirect_print)
        return instance.logger