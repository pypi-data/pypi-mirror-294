import colorama
import os
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
        print('CupDef version', version('CupDefs'))
