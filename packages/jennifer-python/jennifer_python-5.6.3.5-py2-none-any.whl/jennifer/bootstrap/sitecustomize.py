import os
import sys
import traceback
from os import path
from datetime import datetime

_debug_mode = os.getenv('JENNIFER_PY_DBG')


def format_time(time_value):
    return time_value.strftime("[%Y-%m-%d %H:%M:%S]")


def _log(level, *args):
    current_time = format_time(datetime.now())
    print(current_time, '[' + str(os.getpid()) + ']', level, '[jennifer]', args)


try:
    jennifer = __import__('jennifer')
except ImportError as e:
    jennifer_path = path.abspath(path.join(path.dirname(__file__), '..', '..'))
    sys.path.append(jennifer_path)
    jennifer = __import__('jennifer')

if os.environ.get('JENNIFER_MASTER_ADDRESS') is not None:
    try:
        jennifer.startup.init()
    except Exception as e:
        _log('[ERROR]', 'site_customize', e)
        if _debug_mode:
            traceback.print_exc()

