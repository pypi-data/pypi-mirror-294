import json
import logging
from datetime import datetime, timedelta
from flask import Response, jsonify, request, send_file
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL  # 0, 10, 20, 30, 40, 50
from io import BytesIO
from pathlib import Path
from pypomes_core import (
    APP_PREFIX, DATETIME_FORMAT_INV, TEMP_FOLDER, DATETIME_FORMAT_COMPACT,
    env_get_str, exc_format, datetime_parse, str_get_positional
)
from pypomes_http import http_get_parameters
from sys import exc_info, stderr
from typing import Any, Final, Literal, TextIO

__LOGGING_ID: Final[str] = APP_PREFIX
__LOGGING_DEFAULT_STYLE: Final[str] = ("{asctime} {levelname:1.1} {thread:5d} "
                                       "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
LOGGING_LEVEL: int | None = None
LOGGING_FORMAT: str | None = None
LOGGING_STYLE: str | None = None
LOGGING_DATE_FORMAT: str | None = None
LOGGING_FILE_MODE: str | None = None
LOGGING_FILE_PATH: Path = TEMP_FOLDER / f"{APP_PREFIX}.log"
PYPOMES_LOGGER: logging.Logger | None = None


def logging_startup(scheme: dict[str, Any] = None) -> str:
    """
    Start or restart the log service.

    The parameters for configuring the log can be found either as environment variables, or as
    attributes in *scheme*. Default values are used, if necessary.

    :param scheme: optional log parameters and corresponding values
    """
    # initialize the return variable
    result: str | None = None

    scheme = scheme or {}
    global LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_STYLE, \
           LOGGING_DATE_FORMAT, LOGGING_FILE_MODE, LOGGING_FILE_PATH, PYPOMES_LOGGER

    try:
        # noinspection PyTypeChecker
        logging_level: int = __get_logging_level(level=scheme.get("log-level",
                                                                  env_get_str(key=f"{APP_PREFIX}_LOGGING_LEVEL",
                                                                              def_value="debug").lower()))
        logging_format: str = scheme.get("log-format",
                                         env_get_str(key=f"{APP_PREFIX}_LOGGING_FORMAT",
                                                     def_value=__LOGGING_DEFAULT_STYLE))
        logging_style: str = scheme.get("log-style",
                                        env_get_str(key=f"{APP_PREFIX}_LOGGING_STYLE",
                                                    def_value="{"))
        logging_date_format: str = scheme.get("log-date-format",
                                              env_get_str(key=f"{APP_PREFIX}_LOGGING_DATE_FORMAT",
                                                          def_value=DATETIME_FORMAT_INV))
        logging_file_mode: str = scheme.get("log-file-mode",
                                            env_get_str(key=f"{APP_PREFIX}_LOGGING_FILE_MODE",
                                                        def_value="a"))
        logging_file_path: Path = Path(scheme.get("log-file-path",
                                                  env_get_str(key=f"{APP_PREFIX}_LOGGING_FILE_PATH")))

        LOGGING_LEVEL = logging_level
        LOGGING_FORMAT = logging_format
        LOGGING_STYLE = logging_style
        LOGGING_DATE_FORMAT = logging_date_format
        LOGGING_FILE_MODE = logging_file_mode
        LOGGING_FILE_PATH = logging_file_path
    except Exception as e:
        result = exc_format(exc=e,
                            exc_info=exc_info())
    # error ?
    if not result:
        # no, proceed
        force_reset: bool
        # is there a logger ?
        if PYPOMES_LOGGER:
            # yes, shut it down
            logging.shutdown()
            force_reset = True
        else:
            # no, start it
            PYPOMES_LOGGER = logging.getLogger(name=__LOGGING_ID)
            force_reset = False

        # configure the logger
        # noinspection PyTypeChecker
        logging.basicConfig(filename=LOGGING_FILE_PATH,
                            filemode=LOGGING_FILE_MODE,
                            format=LOGGING_FORMAT,
                            datefmt=LOGGING_DATE_FORMAT,
                            style=LOGGING_STYLE,
                            level=LOGGING_LEVEL,
                            force=force_reset)
        for _handler in logging.root.handlers:
            _handler.addFilter(filter=logging.Filter(__LOGGING_ID))

    return result


def logging_get_entries(errors: list[str],
                        log_level: int = None,
                        log_from: datetime = None,
                        log_to: datetime = None) -> BytesIO:
    """
    Extract and return entries in the current logging file.

    Parameters specify criteria for log entry selection, and are optional.
    Intervals are inclusive (*[log_from, log_to]*).
    It is required that the current logging file be compliant with
    *PYPOMES_LOGGER*'s *__LOGGING_DEFAULT_STYLE*,
    or that criteria for log entry selection not be specified.

    :param errors: incidental error messages
    :param log_level: the logging level (defaults to all levels)
    :param log_from: the initial timestamp (defaults to unspecified)
    :param log_to: the finaL timestamp (defaults to unspecified)
    :return: the logging entries meeting the specified criteria
    """
    # initialize the return variable
    result: BytesIO | None = None

    # verify whether inspecting the log entries is possible
    if LOGGING_STYLE != __LOGGING_DEFAULT_STYLE and \
       (log_level or log_from or log_to):
        errors.append("It is not possible to apply level "
                      "or timestamp criteria to filter log entries")
    # errors ?
    if not errors:
        # no, proceed
        result = BytesIO()
        filepath: Path = Path(LOGGING_FILE_PATH)
        with (filepath.open() as f):
            line: str = f.readline()
            while line:
                items: list[str] = line.split(sep=None,
                                              maxsplit=3)
                # noinspection PyTypeChecker
                msg_level: int = CRITICAL if not log_level or len(items) < 2 \
                                 else __get_logging_level(level=items[2].lower())
                # 'not log_level' works for both values 'NOTSET' and 'None'
                if not log_level or msg_level >= log_level:
                    if len(items) > 1 and (log_from or log_to):
                        timestamp: datetime = datetime_parse(f"{items[0]} {items[1]}")
                        if not timestamp or \
                           ((not log_from or timestamp >= log_from) and
                            (not log_to or timestamp <= log_to)):
                            result.write(line.encode())
                    else:
                        result.write(line.encode())
                line = f.readline()

    return result


def logging_send_entries(scheme: dict[str, Any]) -> Response:
    """
    Retrieve from the log file, and send in response, the entries matching the criteria specified in *scheme*.

    :param scheme: the criteria for filtering the records to be returned
    :return: file containing the log entries requested
    """
    # declare the return variable
    result: Response

    # initialize the error messages list
    errors: list[str] = []

    # obtain the logging level
    log_level: int = str_get_positional(source=scheme.get("log-level", "debug")[:1].upper(),
                                        list_origin=["debug", "info", "warning", "error", "critical"],
                                        list_dest=[10, 20, 30, 40, 50])
    # obtain the  timestamps
    log_from: datetime = datetime_parse(dt_str=scheme.get("log-from-datetime"))
    log_to: datetime = datetime_parse(dt_str=scheme.get("log-to-datetime"))

    if not log_from and not log_to:
        last_days: str = scheme.get("log-last-days", "0")
        last_hours: str = scheme.get("log-last-hours", "0")
        offset_days: int = int(last_days) if last_days.isdigit() else 0
        offset_hours: int = int(last_hours) if last_hours.isdigit() else 0
        if offset_days or offset_hours:
            log_from = datetime.now() - timedelta(days=offset_days,
                                                  hours=offset_hours)
    # retrieve the log entries
    log_entries: BytesIO = logging_get_entries(errors=errors,
                                               log_level=log_level,
                                               log_from=log_from,
                                               log_to=log_to)
    # errors ?
    if not errors:
        # no, return the log entries requested
        base: str = "entries"
        if log_from:
           base += f"-from_{log_from.strftime(format=DATETIME_FORMAT_COMPACT)}"
        if log_to:
           base += f"-to_{log_to.strftime(format=DATETIME_FORMAT_COMPACT)}"
        log_file = f"log_{base}.log"
        param: str = scheme.get("log-attach", "true")
        attach: bool = not (isinstance(param, str) and param.lower() in ["0", "f", "false"])
        log_entries.seek(0)
        result = send_file(path_or_file=log_entries,
                           mimetype="text/plain",
                           as_attachment=attach,
                           download_name=log_file)
    else:
        # yes, report the failure
        result = Response(response=json.dumps(obj={"errors": errors}),
                          status=400,
                          mimetype="application/json")

    return result


def logging_log_msgs(msgs: str | list[str],
                     output_dev: TextIO = None,
                     log_level: int = ERROR) -> None:
    """
    Write all messages in *msgs* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msgs: the messages list
    :param output_dev: output device where the message is to be printed (None for no device printing)
    :param log_level: the logging level, defaults to 'error' ('None' for no logging)
    """
    # define the log writer
    log_writer: callable = None
    match log_level:
        case "debug":
            log_writer = PYPOMES_LOGGER.debug
        case "info":
            log_writer = PYPOMES_LOGGER.info
        case "warning":
            log_writer = PYPOMES_LOGGER.warning
        case "error":
            log_writer = PYPOMES_LOGGER.error
        case "critical":
            log_writer = PYPOMES_LOGGER.critical

    # traverse the messages list
    msg_list: list[str] = [msgs] if isinstance(msgs, str) else msgs
    for msg in msg_list:
        # has the log writer been defined ?
        if log_writer:
            # yes, log the message
            log_writer(msg)

        # write to output
        __write_to_output(msg=msg,
                          output_dev=output_dev)


def logging_log_debug(msg: str,
                      output_dev: TextIO = None) -> None:
    """
    Write debug-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed ('None' for no device printing)
    """
    # log the message
    PYPOMES_LOGGER.debug(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_info(msg: str,
                     output_dev: TextIO = None) -> None:
    """
    Write info-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed ('None' for no device printing)
    """
    # log the message
    PYPOMES_LOGGER.info(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_warning(msg: str,
                        output_dev: TextIO = None) -> None:
    """
    Write warning-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed ('None' for no device printing)
    """
    # log the message
    PYPOMES_LOGGER.warning(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_error(msg: str,
                      output_dev: TextIO = None) -> None:
    """
    Write error-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed ('None' for no device printing)
    """
    # log the message
    PYPOMES_LOGGER.error(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)


def logging_log_critical(msg: str,
                         output_dev: TextIO = None) -> None:
    """
    Write critical-level message *msg* to *logger*'s logging file, and to *output_dev*.

    The output device is tipically *sys.stdout* or *sys.stderr*.

    :param msg: the message to log
    :param output_dev: output device where the message is to be printed ('None' for no device printing)
    """
    # log the message
    PYPOMES_LOGGER.critical(msg=msg)
    __write_to_output(msg=msg,
                      output_dev=output_dev)

# @app.route(rule="/logging",
#            methods=["GET", "POST"])
def logging_service() -> Response:
    """
    Entry pointy for configuring and retrieving the execution log of the system.

    The optional *GET* criteria, used to filter the records to be returned, are specified according
    to the pattern *attach=<[t,true,f,false]>&log-level=<debug|info|warning|error|critical>&
    log-from-datetime=YYYYMMDDhhmmss&log-to-datetime=YYYYMMDDhhmmss&log-last-days=<n>&log-last-hours=<n>>*:
        - *log-attach*: whether browser should display or persist file (defaults to True - persist it)
        - *log-level*: the logging level of the entries (defaults to *info*)
        - *log-from-datetime*: the start timestamp
        - log-to-datetime*: the finish timestamp
        - *log-last-days*: how many days before current date
        - *log-last-hours*: how may hours before current time
    The *POST* operation configures and starts/restarts the logger.
    These are the optional query parameters (missing parameters are obtained from environment variables):
        - *log-level*: the loggin level (*debug*, *info*, *warning*, *error*, *critical*)
        - *log-file-path*: path for the log file
        - *log-file-mode*: the mode for log file opening (a- append, w- truncate)
        - *log-format*: the information and formats to be written to the log
        - *log-style*: the style used for building the 'log-format' parameter
        - *log-date-format*: the format for displaying the date and time (defaults to YYYY-MM-DD HH:MM:SS)

    :return: the requested log data, on 'GET', and the operation status, on 'POST'
    """
    # register the request
    req_query: str = request.query_string.decode()
    logging_log_info(f"Request {request.path}?{req_query}")

    # obtain the request parameters
    scheme: dict = http_get_parameters(request=request)

    # run the request
    result: Response
    if request.method == "GET":
        result = logging_send_entries(scheme=scheme)
    else:
        reply: str = logging_startup(scheme=scheme)
        if reply:
            result = jsonify({"errors": [reply]})
            result.status_code = 400
        else:
            result = Response(status=200)

    # log the response
    logging_log_info(f"Response {request.path}?{req_query}: {result}")

    return result


def __get_logging_level(level: Literal["debug", "info", "warning", "error", "critical"]) -> int:
    """
    Translate the log severity string *level* into the logging's internal severity value.

    :param level: the string log severity
    :return: the internal logging severity value
    """
    result: int | None
    match level:
        case "debug":
            result = DEBUG          # 10
        case "info":
            result = INFO           # 20
        case "warning":
            result = WARNING        # 30
        case "error":
            result = ERROR          # 40
        case "critical":
            result = CRITICAL       # 50
        case _:
            result = NOTSET         # 0

    return result

def __write_to_output(msg: str,
                      output_dev: TextIO) -> None:

    # has the output device been defined ?
    if output_dev:
        # yes, write the message to it
        output_dev.write(msg)

        # is the output device 'stderr' ou 'stdout' ?
        if output_dev.name.startswith("<std"):
            # yes, skip to the next line
            output_dev.write("\n")


# initialize the logger
__reply: str = logging_startup()
if __reply:
    stderr.write(__reply + "\n")

