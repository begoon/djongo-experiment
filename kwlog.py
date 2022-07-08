import logging
from typing import Any

EMAIL_LOG_LEVEL = 'error'


class KwLog:
    def __init__(self, logger):
        self.logger = logger

    def format_kwargs(self, kwargs):
        def as_string(value):
            if isinstance(value, str):
                return f'"{value}"'
            return str(value)

        def is_printable(x: Any) -> bool:
            return True

        items = filter(is_printable, kwargs.items())
        return ' '.join(f'{k}={as_string(v)}' for k, v in items)

    def format_message(self, *args, **kwargs):
        parts = [str(arg) for arg in args] if args else []
        if len(parts) > 1:
            parts.extend(['-', parts.pop(0)])
        if kwargs:
            if parts:
                parts.append('|')
            parts.append(self.format_kwargs(kwargs))
        return ' '.join(parts)

    def send_email(self, *args, **kwargs):
        raise NotImplementedError()

    def __getattr__(self, attr: str):
        def wrapper(*args, **kwargs):
            is_email = attr == 'email'
            action = (EMAIL_LOG_LEVEL if is_email else attr).lower()
            method = getattr(self.logger, action)
            if action in ['debug', 'info', 'warning', 'error']:
                if is_email:
                    self.send_email(*args, **kwargs)
                return method(self.format_message(*args, **kwargs))
            return method(*args, **kwargs)

        return wrapper


def logger(logger_name='-') -> logging.Logger:
    return KwLog(logging.getLogger(logger_name))


getLogger = logger

get_logger = logger
