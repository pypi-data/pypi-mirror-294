import structlog
import logging
import re

from abstract_logger.anonymizer import Anonymizer
from abstract_logger.config_loader import LogConfig


class Logger:
    def __init__(self, config_file_path=None):
        self.config = LogConfig(config_file_path).get_config()
        self.anonymizer = Anonymizer(self.config)
        self.anonymize_fields = self.config.get("anonymize_fields", [])
        self.anonymize_patterns = self.config.get("anonymize_patterns", {})
        self.logger = self._configure_logger()

    def _configure_logger(self):
        # Configure basic logging level
        logging.basicConfig(level=self.config["log_level"])

        # Structlog processors
        processors = [
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        # Configure logging type
        if self.config["log_format"] == "json":
            processors.append(structlog.processors.JSONRenderer())
        else:
            # Disable ANSI codes if logging to a file
            if self.config["log_destination"] == "file":
                processors.append(structlog.dev.ConsoleRenderer(colors=False))
            else:
                processors.append(structlog.dev.ConsoleRenderer(colors=True))

        # Configure logging destination
        if self.config["log_destination"] == "file":
            file_handler = logging.FileHandler(self.config["log_file_path"])
            structlog.configure(
                processors=processors,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )
            logging.getLogger().addHandler(file_handler)
        else:
            structlog.configure(
                processors=processors,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=True,
            )

        return structlog.get_logger()
    # To handle PHI/PII anonymization within log mesages
    def anonymize_message(self, message):
        # Anonymize message using patterns from the config
        for key, pattern in self.anonymize_patterns.items():
            message = re.sub(pattern, lambda x: self.anonymizer.anonymize(x.group()), message)

        return message

    # Anonymizer for arguments
    def anonymize(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.anonymize_fields:
                kwargs[key] = self.anonymizer.anonymize(value)
        return kwargs

    def info(self, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        self.logger.info(message, **kwargs)

    def debug(self, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        self.logger.debug(message, **kwargs)

    def warning(self, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        self.logger.warning(message, **kwargs)

    def error(self, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        self.logger.error(message, **kwargs)

    def critical(self, message, **kwargs):
        message = self.anonymize_message(message)
        kwargs = self.anonymize(**kwargs)
        self.logger.critical(message, **kwargs)
