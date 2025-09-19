import logging

def init_logger():
    """Initialize and return a logger with file and console handlers."""

    # Create a logger
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler: To log to a file
    file_handler = logging.FileHandler('flet-manage-digital-ingest.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler: To print to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Can set different level for console
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

    ## Test messages
    # logger.debug('Debug message')
    # logger.info('Info message')
    # logger.warning('Warning message')
    # logger.error('Error message')
    # logger.critical('Critical message')