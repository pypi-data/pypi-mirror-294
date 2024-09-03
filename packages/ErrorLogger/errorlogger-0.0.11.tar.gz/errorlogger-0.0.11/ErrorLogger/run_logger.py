from ErrorLogger import ErrorLogger

# Initialize the logger with the path to your config file
logger = ErrorLogger(config_file='config.ini')

# Start collecting logs
# The logger runs in a separate thread and collects logs automatically
# So there's no need to call collect_logs() directly here
print("ErrorLogger is running and collecting logs.")
