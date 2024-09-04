import colorama
from CupDefs import utils
from CupDefs import vars
from CupDefs import vergen


def init(*args: str) -> bool:
    use_color = True

    if 'no_color' in args:
        utils.pwarn = utils.pdone = utils.perror = utils.pinfo = print
        use_color = False
    else:
        colorama.init(autoreset=True)
    if 'no_vergen' not in args:
        vergen.init_vergen()
    if 'no_logo' not in args:
        utils.print_logo(use_color)
    return True
