import os
import logging
import logging.config


def configure_logger(log_config_path: str) -> None:
    assert os.path.exists(log_config_path), "Log file does not exist."
    logging.config.fileConfig(
        os.path.join(log_config_path),
        disable_existing_loggers=False,
    )


def get_logger(
    log_config_path: str,
    logger_name: str = "console_and_file",
    diplayed_logger_name: str = "console_and_file",
) -> logging.Logger:
    configure_logger(log_config_path)
    logger = logging.getLogger(logger_name)
    logger.name = diplayed_logger_name
    return logger
