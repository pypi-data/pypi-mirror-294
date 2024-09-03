import logging
import configparser
import threading
import time
import requests
import pickle
import os

class ErrorLogger:
    def __init__(self, config_file='config.ini'):
        # Read the config file
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Get the APM base URL
        self.apm_baseurl = config['DEFAULT']['apm_baseurl']
        
        # Configure the logger
        self.logger = logging.getLogger('ErrorLogger')
        self.logger.setLevel(logging.INFO)  # Set to INFO to log more details
        
        # File handler for log messages
        file_handler = logging.FileHandler('error_logs.log')
        file_handler.setLevel(logging.ERROR)  # Only log errors to file
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler (optional, for debugging purposes)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log info and above to console
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Initialize logs storage
        self.logs_storage_file = 'logs.pkl'
        
        # Start a thread to continuously collect logs
        self.collector_thread = threading.Thread(target=self._start_collecting_logs)
        self.collector_thread.daemon = True
        self.collector_thread.start()

    def _start_collecting_logs(self):
        while True:
            self.collect_logs()
            time.sleep(60)  # Fetch logs every 60 seconds

    def collect_logs(self):
        try:
            response = requests.get(self.apm_baseurl)
            response.raise_for_status()
            
            # Log response content type
            self.logger.error(f"Response Content-Type: {response.headers.get('Content-Type', '')}")
            
            # Attempt to parse the response as JSON, regardless of content type
            try:
                logs = response.json()
                # Save logs using pickle
                self._save_logs(logs)
            except ValueError:
                self.logger.error(f"Response Content: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            # Log the request exception message
            self.logger.error(f"Exception: {str(e)}")

    def _save_logs(self, logs):
        try:
            with open(self.logs_storage_file, 'ab') as file:
                pickle.dump(logs, file)
        except Exception as e:
            self.logger.error(f"Failed to save logs: {e}")

    def log_exception(self, exception: Exception, message: str = None):
        error_message = message if message else str(exception)
        self.logger.error(f"Exception: {error_message}")

    def convert_logs_to_pickle(self, log_file='error_logs.log', pickle_file='logs.pkl'):
        """Convert the contents of the log file to a pickle file."""
        log_data = []

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

def capture_exception(logger: ErrorLogger, message: str = None):
    def wrapper(func):
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log_exception(e, message)
                raise e  # Re-raise the exception after logging it
        return inner_function
    return wrapper
