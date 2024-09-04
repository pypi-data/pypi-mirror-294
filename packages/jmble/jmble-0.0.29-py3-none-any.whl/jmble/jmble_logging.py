""" Utilities to configure logging using the Configurator """

import logging
import logging.config
import os

from jmble.config import Configurator
from jmble.general_modules import utils
from jmble._types import AttrDict

CONFIG = Configurator()
ENV_PROPS = CONFIG.get_environment()


def configure_logging(
    app_name: str = None, default_logger_name: str = "console_logger"
) -> logging.Logger:
    """Configure logging using the Configurator.

    Args:
        app_name (str, optional): Name of the application. Defaults to None.
        default_logger_name (str, optional): Name of the default logger to return. Defaults to "console_logger".

    Returns:
        logging.Logger: Logger instance.
    """

    app_props = CONFIG.get(app_name) if app_name else AttrDict()

    log_config = ENV_PROPS.get("base_python_log_cfg", AttrDict())

    if not isinstance(log_config, AttrDict) and isinstance(log_config, dict):
        log_config = AttrDict(log_config)

    app_handlers = app_props.logging.handlers
    app_loggers = app_props.logging.loggers

    if isinstance(app_handlers, dict):
        log_config.handlers.update(app_handlers)

    if isinstance(app_loggers, dict):
        log_config.loggers.update(app_loggers)

    _check_log_paths(log_config)

    logging.config.dictConfig(log_config)

    return logging.getLogger(default_logger_name)


def _check_log_paths(log_config: AttrDict) -> None:
    """Check the log paths and create them if they do not exist.

    Args:
        log_config (AttrDict): Log configuration.
    """

    for handler in log_config.handlers.values():
        if "filename" in handler:
            log_path = os.path.expanduser(handler.filename)
            log_dir = os.path.dirname(log_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
