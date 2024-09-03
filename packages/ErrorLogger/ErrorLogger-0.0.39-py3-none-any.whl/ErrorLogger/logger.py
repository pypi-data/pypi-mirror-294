import logging
import configparser
import threading
import time
import requests
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
        if 'DEFAULT' not in config or 'apm_baseurl' not in config['DEFAULT'] or 'api_endpoint' not in config['DEFAULT']:
            raise ValueError("Configuration file is missing required settings.")
 
        # Get the APM base URL and API endpoint
        self.apm_baseurl = config['DEFAULT']['apm_baseurl']
        self.api_endpoint = config['DEFAULT']['api_endpoint']
 
        # Configure the logger
        self.logger = logging.getLogger('ErrorLogger')
        self.logger.setLevel(logging.INFO)
 
        # Console handler for debugging purposes
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
 
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
 
            # Send the logs to the API endpoint
            self._send_logs_to_api(logs)
 
        except requests.exceptions.RequestException as e:
            # Handle request errors
            error_info = f"Request exception: {str(e)}"
            self.logger.error(error_info)
            self._send_logs_to_api({'error': error_info})
 
    def _send_logs_to_api(self, logs):
        try:
            response = requests.post(self.api_endpoint, json=logs)
            response.raise_for_status()
            self.logger.info("Logs successfully sent to API.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send logs to API: {e}")
 
    def log_exception(self, exception: Exception, message: str = None):
        error_message = message if message else str(exception)
        self.logger.error(f"Exception: {error_message}")
        # Send the exception directly to the API endpoint
        self._send_logs_to_api({'exception': error_message})
 
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