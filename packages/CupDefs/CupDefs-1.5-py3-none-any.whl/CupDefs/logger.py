from CupDefs import utils
from CupDefs import vars
import enum
import io
import datetime
import typing


class LogType(enum.Enum):
    DONE = utils.pdone
    ERROR = utils.perror
    WARNING = utils.pwarn
    INFO = utils.pinfo


class Logger:
    _LOGS_PATH = './last_launch.log'
    _logger_file: io.TextIOWrapper = None
    _is_logs_inited = False

    @staticmethod
    def mklog(log_type: LogType | typing.Callable, text: str):
        time = datetime.datetime.now(datetime.timezone.utc)
        time = time.strftime("%d.%m.%y-%H:%M:%S")
        match log_type:
            case utils.pdone:
                prefix = 'OK '
            case utils.perror:
                prefix = 'ERR'
            case utils.pwarn:
                prefix = 'WRN'
            case _:
                prefix = 'INF'
        prefix = '[' + prefix + '][' + time + '] '
        text = prefix + text
        if vars.PRINT_CUPDEFS_ERROR:
            log_type(text)
        if not Logger._is_logs_inited:
            if vars.PRINT_CUPDEFS_ERROR:
                utils.pwarn('Невозможно осуществить запись в файл логов - он не открыт')
            return
        Logger._logger_file.write(text + '\n')

    @staticmethod
    def mklogif(condition: bool | typing.Callable, log_type, text: str):
        if callable(condition):
            condition = condition()
        if condition:
            Logger.mklog(log_type, text)

    @staticmethod
    def init_logs(logs_path: str | None) -> bool:
        if Logger._is_logs_inited:
            return True
        try:
            if logs_path:
                Logger._LOGS_PATH = logs_path
            with open(Logger._LOGS_PATH, 'w'):  # открытие, очистка и закрытие
                pass
            Logger._logger_file = open(Logger._LOGS_PATH, 'a', encoding='utf-8')
            Logger._is_logs_inited = True
            if vars.PRINT_CUPDEFS_ERROR:
                utils.pdone('Файл логов успешно создан')
            Logger.mklog(LogType.INFO, 'Начало логирования. Время по UTC')
            return True
        except IOError:
            if vars.PRINT_CUPDEFS_ERROR:
                utils.perror('Файл логов не создан')
            return False

    @staticmethod
    def close_logs() -> bool:
        if not Logger._is_logs_inited:
            return True
        try:
            Logger.mklog(LogType.INFO, 'Конец логирования')
            Logger._logger_file.close()
            Logger._is_logs_inited = False
            if vars.PRINT_CUPDEFS_ERROR:
                utils.pdone('Файл логов успешно закрыт')
            return True
        except IOError:
            if vars.PRINT_CUPDEFS_ERROR:
                utils.pwarn('Файл логов не удалось закрыть')
            return False
