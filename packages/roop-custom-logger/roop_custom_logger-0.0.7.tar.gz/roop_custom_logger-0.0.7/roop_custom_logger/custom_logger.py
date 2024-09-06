import logging
import os
from asgi_correlation_id import CorrelationIdFilter

LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "DEBUG")

class AppFilter(object):
    def filter(self, record):
        return True

class CustomLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        # Extract extra info from kwargs
        extra_info = kwargs.pop("extra", None)

        # Append extra_info to msg
        if extra_info:
            msg += f": {extra_info}"

        # Call parent process method
        return super().process(msg, kwargs)

def getLogger():
    dlogger = logging.getLogger("baseLogger")
    dlogger.propagate = False  # remove default logger

    # dlogger.addFilter(AppFilter())
    dlogger.addFilter(CorrelationIdFilter())
    
    syslog = logging.StreamHandler()
    fmt_str1 = '%(levelname)s:%(asctime)s:%(correlation_id)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s'
    formatter = logging.Formatter(fmt_str1)

    syslog.setFormatter(formatter)
    dlogger.setLevel(LOG_LEVEL)
    
    if not dlogger.hasHandlers():
        dlogger.addHandler(syslog)
        
    dlogger = CustomLoggerAdapter(dlogger)
    return dlogger