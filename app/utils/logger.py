import logging
import sys

def get_logger(name: str = __name__, level: int = logging.INFO, log_file: str = None) -> logging.Logger:
    """
    Returns a reusable logger instance.

    Args:
        name (str): Name of the logger.
        level (int): Logging level.
        log_file (str): If provided, logs will also be written to this file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    logger.propagate = False
    return logger