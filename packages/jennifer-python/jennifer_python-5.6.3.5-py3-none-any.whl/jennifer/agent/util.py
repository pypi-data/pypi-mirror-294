import os
from datetime import datetime
import traceback


def _log_tb(*args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', '[ERROR]', '[jennifer]', args)
    traceback.print_exc()


def format_time(time_value):
    return time_value.strftime("[%Y-%m-%d %H:%M:%S]")


def _log(level, *args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', level, '[jennifer]', args)


def _debug_log(text):
    if os.getenv('JENNIFER_PY_DBG'):
        try:
            log_socket = __import__('jennifer').get_log_socket()
            if log_socket is not None:
                log_socket.log(text)
        except ImportError as e:
            print(e)
