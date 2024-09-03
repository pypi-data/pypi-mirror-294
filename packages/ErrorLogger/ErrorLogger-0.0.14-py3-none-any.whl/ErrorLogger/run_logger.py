from ErrorLogger import ErrorLogger

# Initialize the logger with the path to your config file
logger = ErrorLogger(config_file='config.ini')

# Log a test message to ensure everything is working
logger.logger.info("ErrorLogger initialized and running.")

# The logger runs in a separate thread and collects logs automatically
# So there's no need to call collect_logs() directly here

# Keep the script running to allow the logger thread to keep collecting logs
try:
    while True:
        # Simulate the main application doing something
        pass
except KeyboardInterrupt:
    print("Stopping the logger.")
