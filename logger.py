import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:
    """
    A custom logger class that sets up logging to both console and a timed rotating file.

    :param log_file: The file path for the log file.
    :type log_file: str
    """

    def __init__(self, log_file):
        """
        Initializes the CustomLogger with a specified log file.

        :param log_file: The file path for the log file.
        :type log_file: str
        """
        self.logger = logging.getLogger("CL")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            # Handler for console output
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            # Handler for file output with timed rotation
            file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=14)
            file_handler.setLevel(logging.INFO)

            # Format for log messages
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def close_logger(self):
        """
        Closes the logger by removing all handlers.

        :return: None
        """
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
