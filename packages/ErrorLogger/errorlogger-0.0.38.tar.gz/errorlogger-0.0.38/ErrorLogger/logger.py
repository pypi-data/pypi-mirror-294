import logging
import configparser
import threading
import time
import requests
import os
from functools import wraps
 
class ErrorLogger:
    def __init__(self, config_file='config.ini'):
        self.load_config(config_file)
        self.setup_logger()
        self.start_log_collector()
 
    def load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError("Configuration file not found.")
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        if 'DEFAULT' not in self.config or 'apm_baseurl' not in self.config['DEFAULT'] or 'api_endpoint' not in self.config['DEFAULT']:
            raise ValueError("Configuration file is missing required settings.")
        self.apm_baseurl = self.config['DEFAULT']['apm_baseurl']
        self.api_endpoint = self.config['DEFAULT']['api_endpoint']
 
    def setup_logger(self):
        self.logger = logging.getLogger('ErrorLogger')
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
 
    def start_log_collector(self):
        self.running = True
        self.collector_thread = threading.Thread(target=self.collect_logs_loop)
        self.collector_thread.daemon = True
        self.collector_thread.start()
 
    def stop(self):
        self.running = False
        self.collector_thread.join()
 
    def collect_logs_loop(self):
        while self.running:
            self.collect_logs()
            time.sleep(60)
 
    def collect_logs(self):
        try:
            response = requests.get(self.apm_baseurl)
            response.raise_for_status()
            if 'application/json' in response.headers.get('Content-Type', ''):
                self.process_logs(response.json())
            else:
                self.logger.error("Unexpected content type from APM.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch logs: {str(e)}")
 
    def process_logs(self, logs):
        if not isinstance(logs, dict):
            self.logger.error("Invalid log format received from APM.")
            return
        self._send_logs_to_api(logs)
 
    def _send_logs_to_api(self, logs):
        try:
            response = requests.post(self.api_endpoint, json=logs)
            response.raise_for_status()
            self.logger.info("Logs successfully sent to API.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send logs to API: {str(e)}")
 
def capture_exception(logger_instance):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger_instance.log_exception(e)
                raise
        return wrapper
    return decorator