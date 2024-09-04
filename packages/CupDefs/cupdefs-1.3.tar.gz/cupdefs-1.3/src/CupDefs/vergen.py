import datetime
import os
import hashlib
from CupDefs import vars
from CupDefs import utils

_TODAY: None | datetime.datetime = None
_DAYS = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 303, 334, 365]
_FILES: None | list[str] = None


def init_vergen():
    global _TODAY, _FILES
    if _TODAY is None:
        _TODAY = datetime.datetime.now(datetime.timezone.utc)
        _FILES = []
        for root, dirs, files in os.walk(vars.VERGEN_HASH_PATH):
            for file in files:
                _FILES.append(os.path.join(root, file))


def generate() -> str | None:
    if _TODAY:
        num = 365 * (_TODAY.year - 2020) - 31 + _DAYS[(_TODAY.month - 1)] + _TODAY.day
        h = b''
        for path in _FILES:
            with open(path, 'rb') as buf:
                h += hashlib.md5(buf.read()).digest()
        return str(num) + hashlib.shake_256(h).hexdigest(vars.VERGEN_HASH_SIZE)
    else:
        if vars.PRINT_CUPDEFS_ERROR:
            utils.perror('Генератор номера не инициализирован')
