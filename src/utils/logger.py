"""
Logging utility for the Material Certificate Extractor
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from config import LOG_FORMAT, LOG_LEVEL, OUTPUT_DIR

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Setup and configure logger
    
    Args:
        name: Logger name (usually __name__ of the module)
        log_file: Optional log file path. If None, logs to console only
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(OUTPUT_DIR / log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_default_log_filename() -> str:
    """Generate default log filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"extraction_{timestamp}.log"
