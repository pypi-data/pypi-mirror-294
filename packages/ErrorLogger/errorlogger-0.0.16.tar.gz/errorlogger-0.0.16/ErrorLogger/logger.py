import logging
import requests
import configparser
import threading
import time

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
        
        # File handler
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
                if isinstance(logs, list):
                    for log in logs:
                        self.logger.error(f"Log: {log}")
                else:
                    self.logger.error(f"Log: {logs}")
            except ValueError:
                # Log the raw response content if JSON parsing fails
                self.logger.error("Failed to parse response as JSON.")
                self.logger.error(f"Response Content: {response.text}")
                    
        except requests.exceptions.RequestException as e:
            # Log the request exception message
            self.logger.error(f"Request Exception: {str(e)}")

    def log_exception(self, exception: Exception, message: str = None):
        # Log the exception with a message if provided
        error_message = message if message else str(exception)
        self.logger.error(f"Exception: {error_message}")

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
