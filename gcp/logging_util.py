import logging

def setup_logger(log_file="run_log.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)