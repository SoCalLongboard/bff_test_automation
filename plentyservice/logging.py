"""Utilities for logging"""

import logging
import os


class LoggingUtils:

    LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s %(lineno)s %(filename)s %(funcName)s"

    @staticmethod
    def setup_logger():
        log_level = logging.DEBUG
        env_log_level = os.environ.get("LOG_LEVEL")
        if env_log_level:
            log_level = logging.getLevelName(env_log_level)

        env = os.environ.get("ENVIRONMENT_CONTEXT")

        handler = logging.StreamHandler()
        if env != "local":
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(LoggingUtils.LOG_FORMAT)
            handler.setFormatter(formatter)
        else:
            formatter = logging.Formatter(LoggingUtils.LOG_FORMAT)
            handler.setFormatter(formatter)

        # Root logger
        root = logging.getLogger()
        root.setLevel(log_level)
        root.addHandler(handler)

        # Django default logger (if any)
        django = logging.getLogger("django")
        if django:
            django.setLevel(log_level)
            django.addHandler(handler)
