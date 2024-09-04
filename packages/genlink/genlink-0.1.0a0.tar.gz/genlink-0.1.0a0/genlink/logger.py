import logging


class Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    @classmethod
    def format_str(cls, args, kwargs):  # type: ignore
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        args_str = ", ".join(args)
        return f"{args_str}, {kwargs_str}"

    @classmethod
    def debug(cls, *args, **kwargs):  # type: ignore
        cls.logger.debug(cls.format_str(args, kwargs))

    @classmethod
    def info(cls, *args, **kwargs):  # type: ignore
        cls.logger.info(cls.format_str(args, kwargs))

    @classmethod
    def warning(cls, *args, **kwargs):  # type: ignore
        cls.logger.warning(cls.format_str(args, kwargs))

    @classmethod
    def error(cls, *args, **kwargs):  # type: ignore
        cls.logger.error(cls.format_str(args, kwargs))

    @classmethod
    def critical(cls, *args, **kwargs):  # type: ignore
        cls.logger.critical(cls.format_str(args, kwargs))
