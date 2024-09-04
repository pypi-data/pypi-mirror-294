import logging
from tai_alphi.formatters import (
    DictFormatter,
    ConsoleFormatter,
    TeamsFormatter,
)
from tai_alphi.handlers import (
    TeamsHandler,
    ConsoleHandler,
    CosmosHandler,
)
from logtail import LogtailHandler
from tai_alphi.exceptions import (
    ConfigFileError,
    LogtailMissingToken,
    MissingConfig
)
from tai_alphi.config import ConfigValidator, NoSQLDBConnectionConfig, LogtailConnectionConfig

class AlphiLogger(logging.Logger):

    def __init__(self, config: ConfigValidator, name: str, level: int = logging.DEBUG, 
                 nosqlDB_conn_config: NoSQLDBConnectionConfig = None,  logtail_token: LogtailConnectionConfig = None):
        
        super().__init__(name, level)
        self._nosqlDB_conn_config = nosqlDB_conn_config
        self._logtail_token = logtail_token
        self.config = config

        self.__set_logger()

    def __set_formatter(self, handler_type, config):
        # if handler_type != 'nosqlDB':
        #     if 'custom_format' in config.model_fields_set:
        #         formatter = TeamsFormatter(custom_format=config.custom_format, datefmt=config.time_format)
        #     else:
        #         formatter = ConsoleFormatter(time_format=config.time_format)
        # elif handler_type == 'nosqlDB':
        #     time_format = config.time_format
        #     formatter = DictFormatter(time_format=time_format)
        if handler_type == 'teams':
                formatter = TeamsFormatter(custom_format=config.custom_format, datefmt=config.time_format)
        elif handler_type == 'nosqlDB':
            time_format = config.time_format
            formatter = DictFormatter(time_format=time_format)
        elif handler_type == 'consola':
            formatter = ConsoleFormatter(time_format=config.time_format)

            if 'display_info' in config:
                formatter.set_log_record_attributes(config.display_info)
        else:
            raise ValueError(f"Unknown formatter type: {handler_type}")

        return formatter

    def __create_handler(self, handler_type: str, config):
        """
        Crea y configura un manejador de logs basado en el tipo de manejador y su configuración.
        """
        handler = None
        formatter = None

        if handler_type == 'consola':
            handler = ConsoleHandler()
        elif handler_type == 'teams':
            handler = TeamsHandler()
        elif handler_type == 'logtail':
            handler = LogtailHandler(self.logtail_token)
        elif handler_type == 'nosqlDB':
            handler = CosmosHandler(
                db_name=self._nosqlDB_conn_config.db_name,
                db_collection_name=self._nosqlDB_conn_config.db_collection_name,
                db_user=self._nosqlDB_conn_config.db_user,
                db_password=self._nosqlDB_conn_config.db_password,
                db_host=self._nosqlDB_conn_config.db_host,
                db_port=self._nosqlDB_conn_config.db_port
            )
        # Añadir el handler a la lista
        if handler:
            formatter = self.__set_formatter(handler_type, config)
            handler.setFormatter(formatter)
            handler.setLevel(config.log_level.upper() if config.log_level is not None else None)
            self.handlers.append(handler)

        return handler

    def __set_handlers(self):

        logger_config = self.config.root[self.name]

        for c in logger_config.model_fields_set:

            config_file_handler = getattr(logger_config, c) 

            if config_file_handler.enabled:
                match c:
                    case 'consola':
                        console_handler = self.__create_handler(c, config_file_handler)
                        self.addHandler(console_handler)

                    case 'teams':
                        teams_handler = self.__create_handler(c, config_file_handler)
                        self.addHandler(teams_handler)

                    case 'nosqlDB':
                        if self._nosqlDB_conn_config:
                            nosqlDB_handler = self.__create_handler(c, config_file_handler)
                            self.addHandler(nosqlDB_handler)                           
                        else:
                            MissingConfig('La ruta NoSQLDB no está configurada')

                    case 'logtail':
                        if self._logtail_token:
                            logtail_handler = self.__create_handler(c, config_file_handler)
                            self.addHandler(logtail_handler)
                        else:
                            LogtailMissingToken()


    def __set_logger(self) -> None:

        if not self.config.root:
            raise ConfigFileError('No se ha cargado el config file')
        elif self.name not in self.config.root:
            raise ConfigFileError(f'No existe logger en config file con el nombre {self.name}')
        
        self.__set_handlers()
