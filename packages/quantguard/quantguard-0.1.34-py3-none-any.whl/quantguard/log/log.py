from logging.config import dictConfig

from quantguard.config import settings


def init_log():
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "sample": {
                "format": "[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "verbose": {
                "format": "[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "formatter": "verbose",
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file": {
                "formatter": "verbose",
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": settings.LOG_FILE,  # 指定日志文件的路径
                "mode": "a",  # 'a' 表示追加模式, 'w' 表示覆盖模式
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {"level": settings.LOG_LEVEL, "handlers": settings.LOG_HANDLER},
        },
    }

    dictConfig(log_config)
