from ErrorLogger import ErrorLogger
import time

# Initialize the logger with the path to your config file
logger = ErrorLogger(config_file='config.ini')

# Log a test message to ensure everything is working
logger.logger.info("ErrorLogger initialized and running.")

# Give the logger some time to start collecting logs
time.sleep(2)

# Log additional messages for testing
logger.logger.info("This is a test info message.")
logger.logger.error("This is a test error message.")

# The logger runs in a separate thread and collects logs automatically
# So there's no need to call collect_logs() directly here

try:
    while True:
        # Simulate the main application doing something
        time.sleep(1)  # Added sleep to avoid high CPU usage
except KeyboardInterrupt:
    print("Stopping the logger.")
