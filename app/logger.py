import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger() -> None:
    # Set up basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            # Add a timed rotating file handler to log to a file
            TimedRotatingFileHandler(
                filename=f".logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                when="midnight",
                interval=1,
                backupCount=1,
            ),
            # Add a stream handler to log to the console
            logging.StreamHandler(),
        ]
    )

    # Set the log level for aiogram.event logger to CRITICAL
    aiogram_logger = logging.getLogger("aiogram.event")
    aiogram_logger.setLevel(logging.CRITICAL)
