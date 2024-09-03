import logging
import datetime
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
        logging.basicConfig(filename='error_logs.log', level=logging.ERROR,
                            format='%(asctime)s %(levelname)s: %(message)s')
        self.logger = logging.getLogger()
        
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
            
            # Log response status and content
            self.logger.info(f"Response Status Code: {response.status_code}")
            self.logger.info(f"Response Content: {response.text[:1000]}")  # Limit to first 1000 characters
            
            # Attempt to parse JSON if applicable
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    logs = response.json()
                    # Assuming logs are in a list format
                    for log in logs:
                        self.logger.error(f"Log: {log}")
                except ValueError:
                    self.logger.error("Failed to parse JSON. Response content might not be valid JSON.")
            else:
                # Log non-JSON content
                self.logger.error(f"Received content type {response.headers.get('Content-Type')}:")
                self.logger.error(response.text)
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to collect logs: {e}")

    def log_exception(self, exception: Exception, message: str = None):
        error_message = message if message else str(exception)
        self.logger.error(f"Exception: {error_message}")
        self.logger.error(f"Type: {type(exception).__name__}")
        self.logger.error(f"Details: {str(exception)}")
        self.logger.error(f"Timestamp: {datetime.datetime.now()}")

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
