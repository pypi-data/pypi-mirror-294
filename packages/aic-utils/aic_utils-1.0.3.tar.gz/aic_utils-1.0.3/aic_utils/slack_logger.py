import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import builtins


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


def redirect_print_to_logger(logger):
    def print_to_logger(*args, **kwargs):
        message = " ".join(str(arg) for arg in args)
        logger.info(message)
    
    # Override the built-in print function
    builtins.print = print_to_logger


def setup_slack_logger(slack_token='xoxb-7424459969442-7456034210037-EMCjbI9oi1xTszU1iUh4tLFH', slack_channel='C07DYFK5SE8', redirect_print=True):
    # Initialize SlackBot and SlackLoggerHandler
    slack_bot = SlackBot(slack_token)
    slack_handler = SlackLoggerHandler(slack_bot, slack_channel)

    # Create a logger and attach the custom Slack handler
    logger = logging.getLogger('SlackLogger')
    logger.setLevel(logging.INFO)  # Set the logging level
    logger.addHandler(slack_handler)

    # Set a basic format for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    slack_handler.setFormatter(formatter)

    # Automatically redirect print statements if specified
    if redirect_print:
        redirect_print_to_logger(logger)

    return logger
