import logging
import configparser
import threading
import time
import requests
import pickle
import os
import datetime
from functools import wraps

class ErrorLogger:
    def __init__(self, config_file='config.ini'):
        # Read the config file
        config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise FileNotFoundError("Configuration file not found.")
        config.read(config_file)

        # Validate necessary configuration is present
        if 'DEFAULT' not in config or 'apm_baseurl' not in config['DEFAULT']:
            raise ValueError("Configuration file is missing required 'apm_baseurl'.")

        # Get the APM base URL
        self.apm_baseurl = config['DEFAULT']['apm_baseurl']

        # Configure the logger
        self.logger = logging.getLogger('ErrorLogger')
        self.logger.setLevel(logging.INFO)

        # File handler for log messages
        file_handler = logging.FileHandler('error_logs.log')
        file_handler.setLevel(logging.ERROR)
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler for debugging purposes
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # Initialize logs storage
        self.logs_storage_file = 'logs.pkl'

        # Start a thread to continuously collect logs
        self.running = True
        self.collector_thread = threading.Thread(target=self._start_collecting_logs)
        self.collector_thread.daemon = True
        self.collector_thread.start()

    def stop(self):
        """ Stop the logging thread. """
        self.running = False
        self.collector_thread.join()

    def _start_collecting_logs(self):
        while self.running:
            self.collect_logs()
            time.sleep(60)  # Fetch logs every 60 seconds

    def collect_logs(self):
        try:
            response = requests.get(self.apm_baseurl)
            response.raise_for_status()
            logs = response.json()
            self._save_logs(logs)  # Save logs directly after fetching
        except requests.exceptions.RequestException as e:
            error_info = f"Exception: {str(e)}"
            self.logger.error(error_info)
            self._save_logs({'error': error_info})

    def _save_logs(self, logs):
        formatted_log = self._format_log(logs)
        try:
            with open(self.logs_storage_file, 'ab') as file:
                pickle.dump(formatted_log, file)
        except Exception as e:
            self.logger.error(f"Failed to save logs: {e}")

    def _format_log(self, log_data):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
        level = 'ERROR'  # Assuming error level; adjust as necessary
        message = log_data if isinstance(log_data, str) else str(log_data)
        return f"{timestamp} {level}: {message}"

    def log_exception(self, exception: Exception, message: str = None):
        error_message = message if message else str(exception)
        self.logger.error(f"Exception: {error_message}")

    def capture_exception(self, message: str = None):
        """Decorator to capture exceptions in Flask routes."""
        def wrapper(func):
            @wraps(func)
            def inner_function(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.log_exception(e, message)
                    raise e  # Re-raise the exception after logging it
            return inner_function
        return wrapper

    def convert_logs_to_pickle(self, log_file='error_logs.log', pickle_file='logs.pkl'):
        """Convert the contents of the log file to a pickle file."""
        if not os.path.isfile(log_file):
            self.logger.error(f"Log file {log_file} not found.")
            return

        with open(log_file, 'r') as file:
            log_data = file.readlines()

        try:
            with open(pickle_file, 'wb') as file:
                pickle.dump(log_data, file)
            self.logger.info(f"Log data successfully converted to {pickle_file}.")
        except Exception as e:
            self.logger.error(f"Failed to convert logs to pickle file: {e}")
