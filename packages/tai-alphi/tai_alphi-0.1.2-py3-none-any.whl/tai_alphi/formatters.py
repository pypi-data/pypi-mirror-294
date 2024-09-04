import logging
from typing import Optional
from tai_alphi.log_config import FORMATS

class Formatter:

    def __init__(self, regular_formatter, console_handler, cosmos_handler):
        self.regular_formatter = Optional[ConsoleFormatter] = None
        self.dict_formatter = Optional[DictFormatter] = None
        self.custom_formatter = Optional[TeamsFormatter] = None

    # def handle_all(self, data):
    #     """Método para manejar datos usando todos los handlers."""
    #     self.regular_formatter.handle(data)
    #     self.console_handler.handle(data)
    #     self.cosmos_handler.handle(data)

    def set_regular_format(self, data):
        """Método para manejar datos solo con ConsoleFormatter."""
        self.regular_formatter.handle(data)

    def set_dict_format(self, data):
        """Método para manejar datos solo con DictFormatter."""
        self.dict_formatter.handle(data)

    def set_custom_format(self, data):
        """Método para manejar datos solo con TeamsFormatter."""
        self.custom_formatter.handle(data)


class BaseFormatter(logging.Formatter):
    keywords = [
        'asctime',
        'filename',
        'funcName',
        'levelname',
        'lineno',
        'message',
        'module',
        'pathname',
    ]
    
    def __init__(self) -> None:
        self._attributes = ['asctime', 'levelname', 'module']
    
    @property
    def attributes(self) -> list:
        return self._attributes
    
    def set_log_record_attributes(self, attributes: list):
        '''
        Params
        -
            fields (list): Listado de atributos a mostrar en cada registro
        
        `fields` args
        -
        >>> asctime
        >>> filename
        >>> funcName
        >>> levelname
        >>> lineno
        >>> module
        >>> pathname
        '''
        valid_attributes = [att for att in attributes if att in self.keywords]
        self._atributes = valid_attributes
    
    def usesTime(self) -> bool:
        return "asctime" in self.attributes


class ConsoleFormatter(BaseFormatter):

    def __init__(self, time_format: str="%H:%M:%S"):
        super().__init__()
        self._time_format = time_format
    
    def format(self, record) -> str:
        record.message = record.getMessage()
        
        if self.usesTime():
            record.asctime = self.formatTime(record, self._time_format)

        std_out = "". join([f'[{getattr(record, att)}]' for att in self.attributes])
        std_out = f"{std_out} {record.message}"

        record.message = std_out
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

     

class DictFormatter(BaseFormatter):

    def __init__(self, time_format: str="%Y-%m-%dT%H:%M:%S"):
        super().__init__()
        self._time_format = time_format

    def format(self, record) -> str:
        record.message = record.getMessage()
        
        if self.usesTime():
            record.asctime = self.formatTime(record, self._time_format)

        message_dict = {attr: getattr(record, attr) for attr in self.attributes}
        message_dict['message'] = record.message
        
        if record.exc_info:

            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return message_dict


class TeamsFormatter(logging.Formatter):

    def __init__(self, custom_format, datefmt) -> None:
        super().__init__(custom_format, datefmt=datefmt, style='%')
    