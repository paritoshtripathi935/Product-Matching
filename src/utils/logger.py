#the file is for logging the information of the program
import logging
import os
import sys
import time
import datetime
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

def create_logger():
    # create a logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    
    # create /logs directory if it does not exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # create a file handler
    log_file = os.path.join("logs", "log_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # create a formatter and set the formatter for the handler
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # add the handler to the logger
    logger.addHandler(file_handler)
    
    # log to the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f'Log Created. Log file: {log_file}')

    return logger

def handle_logging(message, message_type="info", env="dev"):
    """
    Log messages with color-coded formatting based on the message type.

    Parameters:
    - message (str): The message to be logged.
    - message_type (str, optional): The type of message. Possible values are 'info', 'warning', or 'error'.
                                    Defaults to 'info'.

    Notes:
    - This function checks the environment (assumed to be stored in the global variable ENV).
    - In a production environment ('prod'), it uses the logging module for consistent logging.
    - In a non-production environment, it prints directly to the console with color-coded formatting.

    Example:
    >>> handling_logging("This is an informational message", message_type='info')
    >>> handling_logging("This is a warning message", message_type='warning')
    >>> handling_logging("This is an error message", message_type='error')
    """
    
    logger = create_logger()
    
    if env == "production":

        if message_type == "error":
            logger.error(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")
        elif message_type == "info":
            logger.info(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")
        elif message_type == "warning":
            logger.warning(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")

    else:
        if message_type == "error":
            print(f"{Fore.RED}{Style.BRIGHT}ERROR: {message}{Style.RESET_ALL}")

        elif message_type == "info":
            print(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")

        elif message_type == "warning":
            print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")
            