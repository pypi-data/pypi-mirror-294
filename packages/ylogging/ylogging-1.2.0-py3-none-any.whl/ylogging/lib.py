from datetime import datetime
import functools
from google.cloud import error_reporting, logging
import pytz
import sys


# `@functools.wraps(func)` is used to preserve the metadata of the original function,
# this is a good practice when using decorators
def console_and_gcp_log(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # call the original log_struct method
        result = func(self, *args, **kwargs)
        # extract the message from the info dict
        info = args[0] if args else kwargs.get("info")
        message = info.get("message", "no message provided to `log_struct`")
        # print to console with UTC time
        utc_time = datetime.now(pytz.UTC)
        print(f"{utc_time.strftime('%Y-%m-%d %H:%M:%S')} UTC - {message}")
        return result

    return wrapper


# monkey patch the Logger class `log_struct` method
logging.Logger.log_struct = console_and_gcp_log(logging.Logger.log_struct)


def console_and_gcp_error_report(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Call the original report method
        result = func(self, *args, **kwargs)

        # Extract the error message
        error = args[0] if args else kwargs.get("error")
        error_message = str(error)

        # Print to stderr with UTC time
        utc_time = datetime.now(pytz.UTC)
        print(
            f"{utc_time.strftime('%Y-%m-%d %H:%M:%S')} UTC - Error: {error_message}",
            file=sys.stderr,
        )

        return result

    return wrapper


# monkey patch the error reporting `report` method as well
error_reporting.Client.report = console_and_gcp_error_report(
    error_reporting.Client.report
)


def get_gcp_error_reporting_logging_clients(service_name: str):
    error_reporting_client = error_reporting.Client()
    log_name = service_name
    logging_client = logging.Client()
    logger = logging_client.logger(log_name)
    return error_reporting_client, logger


def get_structured_log_msg(
    context: str, message: str, serialized_data: str | None
) -> dict:
    """
    Logs a structured message to the console.
    """
    utc = pytz.UTC
    now = datetime.now(utc)
    log_msg_dict = {
        "context": context,
        "message": message,
        "serialized_data": serialized_data,
        "time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return log_msg_dict
