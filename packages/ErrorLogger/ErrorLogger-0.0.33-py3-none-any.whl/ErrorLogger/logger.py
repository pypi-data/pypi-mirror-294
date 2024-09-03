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
            # Fetch data from the URL
            response = requests.get(self.apm_baseurl)
            response.raise_for_status()  # Raise an exception for HTTP error responses

            # Check the content type
            content_type = response.headers.get('Content-Type', '')

            if 'application/json' in content_type:
                try:
                    # Try to parse JSON data
                    logs = response.json()
                    if not isinstance(logs, dict):
                        # Ensure that the parsed data is a dictionary
                        error_info = f"Invalid JSON format: {response.text}"
                        self.logger.error(error_info)
                        logs = {'error': error_info}
                except ValueError as e:
                    # Handle JSON parsing errors
                    error_info = f"JSON parsing error: {str(e)}"
                    self.logger.error(error_info)
                    logs = {'error': error_info}
            else:
                # Handle cases where the content type is not JSON
                error_info = f"Unexpected content type: {content_type}. Data: {response.text}"
                self.logger.error(error_info)
                logs = {'error': error_info}

            # Save the logs
            self._save_logs(logs)

        except requests.exceptions.RequestException as e:
            # Handle request errors
            error_info = f"Request exception: {str(e)}"
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

    def convert_logs_to_pickle(self, log_file='error_logs.log', pickle_file='logs.pkl'):
        """Convert the contents of the log file to a pickle file."""
        if not os.path.isfile(log_file):
            self.logger.error(f"Log file {log_file} not found.")
            return

        try:
            with open(log_file, 'r') as file:
                log_data = file.readlines()

            with open(pickle_file, 'wb') as file:
                pickle.dump(log_data, file)
            self.logger.info(f"Log data successfully converted to {pickle_file}.")
        except Exception as e:
            self.logger.error(f"Failed to convert logs to pickle file: {e}")

def capture_exception(logger_instance):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Log the exception using the provided logger instance
                logger_instance.log_exception(e)
                # Re-raise the exception to ensure Flask handles it
                raise
        return wrapper
    return decorator
