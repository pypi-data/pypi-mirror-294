# -*- coding: utf-8 -*-

import os
from datetime import datetime
import traceback


def format_time(time_value):
    return time_value.strftime("[%Y-%m-%d %H:%M:%S]")


def _log_tb(*args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', '[ERROR]', '[jennifer]', args)
    traceback.print_exc()


def _log(level, *args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', level, '[jennifer]', args)
