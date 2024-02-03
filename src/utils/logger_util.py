#the file is for logging the information of the program
import logging
import os
import sys
import time
import datetime
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

class LoggerUtil:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logger = self.create_logger()
    
    def create_logger(self):
        """
        Create a logger object that will be used to log messages to a file and the console.
        
        Parameters:
        - None
        
        Returns:
        - logger (logging.Logger): A logger object that can be used to log messages.
        
        Notes:
        - This function creates a logs directory if it does not exist.
        - The log file is named with the current date and time.
        - The log file is stored in the logs directory.
        - The log file is named with the current date and time.
        
        Example:
        >>> create_logger()
        """
           
        logger = logging.getLogger("my_logger")
        logger.setLevel(logging.DEBUG)
        
        if not os.path.exists("logs"):
            os.makedirs("logs")

        log_file = os.path.join("logs", "log_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.info(f'Log Created. Log file: {log_file}')

        return logger

    def handle_logging(self, message, message_type="info", env="dev"):
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
        
        if env == "production":

            if message_type == "error":
                self.logger.error(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")
            elif message_type == "info":
                self.logger.info(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")
            elif message_type == "warning":
                self.logger.warning(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")
            else:
                self.logger.info(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")
        
        else:
            if message_type == "error":
                print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")
            elif message_type == "info":
                print(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")
            elif message_type == "warning":
                print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}INFO: {message}{Style.RESET_ALL}")