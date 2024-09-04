import logging
from pythonjsonlogger import jsonlogger
from sys import stdout
import numpy as np

from ..config.singleton import singleton
from ..dig_ass.db import make_session_id


class JsonFormatter(jsonlogger.JsonFormatter):
    pass
    ####
    # additional json formatting possible
    ####

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json_ensure_ascii = False


@singleton
class LoggerSingleton:
    def __init__(self, loggerConfig) -> None:
        self.logger = logging.getLogger(name=loggerConfig['name'])
        self.logger.setLevel(loggerConfig['level_common'])

        stdoutHandler = logging.StreamHandler(stdout)

        # configure logging to stdout
        # stdout_json == True -> set json Formatter
        stdoutJsonFlag = False
        try:
            stdoutJsonFlag = loggerConfig[
                'stdout_json'
            ]  # optional config field
        except:
            pass

        if stdoutJsonFlag:
            stdoutFormatter = JsonFormatter(loggerConfig['format_stdout'])
        else:
            stdoutFormatter = logging.Formatter(loggerConfig['format_stdout'])

        stdoutHandler.setFormatter(stdoutFormatter)
        stdoutHandler.setLevel(loggerConfig['level_stdout_handler'])
        self.logger.addHandler(stdoutHandler)

        # configure logging to file
        writeToFileFlag = False
        try:
            writeToFileFlag = loggerConfig[
                'write_to_file'
            ]  # optional config field
        except:
            pass

        if writeToFileFlag:
            logFileDir = loggerConfig['file_dir']
            logName = loggerConfig['name']
            logFilePath = f'{logFileDir}/{logName}_{make_session_id()}.json'
            fileHandler = logging.FileHandler(logFilePath, mode='a')
            jsonFormatter = JsonFormatter(loggerConfig['format_file'])
            fileHandler.setFormatter(jsonFormatter)
            fileHandler.setLevel(loggerConfig['level_file_handler'])
            self.logger.addHandler(fileHandler)

    def get(self):
        return self.logger

def log_llm_error(
        text: str | None = None,
        vector: list[float] | None = None,
        model: str = 'gigachat',
        logger=None,
) -> None:
    if text is not None and not text:
        logger.error(f'No response from {model}!!!')
        return None
    if vector is not None and not np.count_nonzero(vector):
        logger.error(f'No response from {model} encoder!!!')
        return None
    return None