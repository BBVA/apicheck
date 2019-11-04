import logging


class CustomLoggerFormatter(logging.Formatter):
    FORMATS_PREFIX = {
        logging.ERROR: "[!]",
        logging.WARNING: "[W]",
        logging.INFO: "[*]",
        logging.DEBUG: "[DEBUG]",
        "DEFAULT": "[*]",
    }
    FORMATS = {
        logging.ERROR: "%(msg)s",
        logging.WARNING: "%(msg)s",
        logging.INFO: "%(msg)s",
        logging.DEBUG: "%(module)s: %(lineno)d: %(msg)s",
        "DEFAULT": "%(msg)s",
    }


class CustomConsoleLoggerFormatter(CustomLoggerFormatter):

    COLOR_MAPPING = {
        'DEBUG': 37,  # white
        'INFO': 36,  # cyan
        'WARNING': 33,  # yellow
        'ERROR': 31,  # red
        'CRITICAL': 41,  # white on red bg
    }

    COLOR_PREFIX = '\033['
    COLOR_SUFFIX = '\033[0m'

    def format(self, record):
        log_prefix = self.FORMATS_PREFIX.get(
            record.levelno,
            self.FORMATS_PREFIX['DEFAULT']
        )
        log_fmt = self.FORMATS.get(
            record.levelno,
            self.FORMATS['DEFAULT']
        )

        formatter = logging.Formatter(
            f"{self.COLOR_PREFIX}{self.COLOR_MAPPING.get(record.levelname, 37)}"
            f"m{log_prefix}{self.COLOR_SUFFIX} "
            f"{log_fmt}"
        )

        return formatter.format(record)


def setup_console_log(log, log_level: str = "INFO"):
    ch = logging.StreamHandler()
    ch.setFormatter(CustomConsoleLoggerFormatter())

    log.setLevel(getattr(logging, log_level))
    log.addHandler(ch)
