import colorama
import os
import sys
import inspect
from CupDefs import vars

from importlib.metadata import version


def perror(text: str):
    print(colorama.Fore.RED + text)


def pwarn(text: str):
    print(colorama.Fore.YELLOW + text)


def pdone(text: str):
    print(colorama.Fore.GREEN + text)


def pinfo(text: str):
    print(colorama.Fore.CYAN + text)


def print_logo(colorize: bool):
    with open(os.path.join(vars.__PACKAGE_DIR, 'logo'), 'r') as logo:
        logo_text = []
        for line in logo.readlines():
            logo_text.append(line.rstrip('\n'))
        for line in logo_text:
            for s in line:
                if s == 'A':
                    if colorize:
                        print(colorama.Back.YELLOW + ' ', end=colorama.Style.RESET_ALL)
                    else:
                        print('#', end='')
                else:
                    print(' ', end='')
            print()
        print('CupDefs version', version('CupDefs'))


def __get_calling_module(depht: int = 2, attr: str | None = '') -> any:
    mod = inspect.getmodule(inspect.stack()[depht][0])  # получаем объект модуля
    if attr == '__file__':
        return os.path.dirname(os.path.abspath(os.path.abspath(mod.__file__)))
    elif attr == '' or attr is None:
        return mod
    return mod.__getattribute__(attr)


def get_code_dir(mode: str, add: str | None = '') -> str:
    """
    Получает абсолютный путь к папке, содержащий скрипт, из которого эта функция вызвана
    :param mode: символы в строке, обозначающие дополнительные действия
    'C' - сменить текущую рабочую директорию на директорию скрипта
    'A' - добавить директорию скрипта в sys.path
    'W' - вернуть без добавления строки-аргумента add
    :param add: дополнительная часть для пути файла. Путь + /add
    :return: абсолютный путь к директории скрипта
    """

    mode = mode.lower()
    pure_buf = __get_calling_module(attr='__file__')
    buf = os.path.join(pure_buf, add) if add else pure_buf
    if 'c' in mode:
        os.chdir(buf)
    if 'a' in mode:
        sys.path.append(buf)
    return pure_buf if 'w' in mode else buf
