import tomli
import logging
from pydantic import BaseModel, Field, model_validator, field_validator, RootModel, root_validator
from typing import Dict, Optional, List, Set

class CommonConfig(BaseModel):
    enabled: Optional[bool] = True
    logger_name: Optional[str] = None
    log_level: Optional[str] = None
    display_info: Optional[List[str]] = None
    custom_format: Optional[str] = None
    time_format: Optional[str] = None

    @staticmethod
    def validate_keys(cls, d: Dict[str, any], allowed_keys: Set[str]):
        if not all(key in allowed_keys for key in d):
            raise ValueError(f'Las etiquetas deben estar en {allowed_keys}')
        return d

    @staticmethod
    def validate_log_level(cls, v: str, list_valid_values: Set[str]):
        if v.upper() not in list_valid_values:
            raise ValueError(f'Las etiquetas deben estar en {list_valid_values}')
        return v.title()    

# Modelo estructura Consola
class ConsolaConfig(CommonConfig):
    @model_validator(mode='before')
    def validate_keys(cls, values):
        allowed_keys = {'enabled', 'logger_name', 'log_level', 'display_info', 'custom_format', 'time_format'}
        return super().validate_keys(cls, values, allowed_keys)
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        list_valid_values = {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT'}
        return super().validate_log_level(cls, v, list_valid_values)
    

# Modelo estructura Teams
class TeamsConfig(CommonConfig):
    @model_validator(mode='before')
    def validate_keys(cls, values):
        allowed_keys = {'enabled', 'logger_name', 'log_level', 'display_info', 'custom_format', 'time_format'}
        return super().validate_keys(cls, values, allowed_keys)
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        list_valid_values = {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT'}
        return super().validate_log_level(cls, v, list_valid_values)
    
# Modelo estructura NoSQL
class NoSQLDBConfig(CommonConfig):
    @model_validator(mode='before')
    def validate_keys(cls, values):
        allowed_keys = {'enabled', 'logger_name', 'log_level', 'display_info', 'custom_format', 'time_format'}
        return super().validate_keys(cls, values, allowed_keys)
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        list_valid_values = {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT'}
        return super().validate_log_level(cls, v, list_valid_values)
    

# Modelo estructura LogTail
class LogtailConfig(CommonConfig):
    @model_validator(mode='before')
    def validate_keys(cls, values):
        allowed_keys = {'enabled', 'logger_name', 'log_level', 'display_info', 'custom_format', 'time_format'}
        return super().validate_keys(cls, values, allowed_keys)
    
    @field_validator('log_level')
    def validate_log_level(cls, v):
        list_valid_values = {'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRIT'}
        return super().validate_log_level(cls, v, list_valid_values)
    

# Modelo Logger
class LoggerConfig(BaseModel):
    consola: Optional[ConsolaConfig] = True
    teams: Optional[TeamsConfig] = False
    nosqlDB: Optional[NoSQLDBConfig] = False
    logtail: Optional[LogtailConfig] = False

    # Valida que solo existan etiquetas permitidas
    @model_validator(mode='before')
    def check_keys(cls, value):
        allowed_keys = {'consola', 'teams', 'nosqlDB', 'logtail'}
        if not all(key in allowed_keys for key in value):
            raise ValueError(f'Las etiquetas deben estar en {allowed_keys}')
        return value
    

# Modelo raíz para validar el diccionario completo
class ConfigValidator(RootModel[Dict[str, LoggerConfig]]):

    # Validación para asegurar que todas las etiquetas de logger sean únicas
    @model_validator(mode='before')
    def check_unique_loggers(cls, values):
        logger_names = values.keys()
        if len(logger_names) != len(set(logger_names)):
            raise ValueError("Los nombres de los loggers deben ser únicos")
        return values

# Modelo para validar la conexión a NoSQLDB
class NoSQLDBConnectionConfig(BaseModel):
    db_name: str = Field(..., description="Nombre de la base de datos NoSQL")
    db_collection_name: str = Field(..., description="Nombre de la colección en la base de datos NoSQL")
    db_user: str = Field(..., description="Nombre de usuario para la base de datos")
    db_password: str = Field(..., description="Contraseña para la base de datos")
    db_host: str = Field(default='localhost', description="Host de la base de datos NoSQL")
    db_port: int = Field(default=27017, description="Puerto de la base de datos NoSQL")

    @field_validator('db_name')
    def validate_db_name(cls, value):
        if not value:
            raise ValueError("NoSQLDBConfig: 'db_name' debe ser una cadena no vacía")
        return value

    @field_validator('db_collection_name')
    def validate_db_collection_name(cls, value):
        if not value:
            raise ValueError("NoSQLDBConfig: 'db_collection_name' debe ser una cadena no vacía")
        return value

    @field_validator('db_user')
    def validate_db_user(cls, value):
        if not value:
            raise ValueError("NoSQLDBConfig: 'db_user' debe ser una cadena no vacía")
        return value

    @field_validator('db_password')
    def validate_db_password(cls, value):
        if not value:
            raise ValueError("NoSQLDBConfig: 'db_password' debe ser una cadena no vacía")
        return value

    @field_validator('db_host')
    def validate_db_host(cls, value):
        if not value:
            raise ValueError("NoSQLDBConfig: 'db_host' debe ser una cadena no vacía")
        return value

    @field_validator('db_port')
    def validate_db_port(cls, value):
        if value <= 0:
            raise ValueError("NoSQLDBConfig: 'db_port' debe ser un número entero positivo")
        return value

# Modelo para validar la conexión a LogTail
class LogtailConnectionConfig(BaseModel):
    logtail_token: str = Field(default="localhost", description="Host de la máquina virtual")

    @field_validator('logtail_token')
    def validate_logtail_token(cls, value):
        if not value:
            raise ValueError("LogtailConnectionConfig: 'logtail_token' debe ser una cadena no vacía")
        return value

# Modelo para validar la conexión a Teams
class TeamsConnectionConfig(BaseModel):
    webhook: str = Field(default="", description="Webhook")
    proyecto: str = Field(default="Test", description="Nombre proyecto")
    pipeline: str = Field(default="Test Alphi", description="Nombre pipeline")
    notify_to: List[str] = Field(default="", description="Emails notificar")



class AlphiConfig:
    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self._config: Optional[ConfigValidator] = None
        self._logtail_token: Optional[LogtailConnectionConfig] = None
        self._nosqlDB_conn_config: Optional[NoSQLDBConnectionConfig] = None
        self._teams_conn_config: Optional[TeamsConnectionConfig] = None

        self._set_config()

    @property
    def config(self) -> Optional[ConfigValidator]:
        """Propiedad para acceder a la configuración validada."""
        return self._config
    
    def _set_config(self) -> None:
        """Carga y valida el archivo de configuración."""
        try:
            with open(self.config_file, mode='rb') as f:
                config = tomli.load(f)
            self._config = ConfigValidator.model_validate(config)
        except (ValueError, FileNotFoundError) as e:
            logging.error(f"Error al cargar o validar la configuración: {e}")
            raise e

    @property
    def nosqlDB_conn_config(self) -> Optional[NoSQLDBConnectionConfig]:
        """Propiedad para acceder a la configuración de NoSQL DB."""
        return self._nosqlDB_conn_config

    def set_nosqlDB_conn_config(self, db_name: str, db_collection_name: str, db_user: str, db_password: str, 
                                db_host: str, db_port: int) -> None:
        """Configura la conexión a la base de datos NoSQL."""
        self._nosqlDB_conn_config = NoSQLDBConnectionConfig(
            db_name=db_name,
            db_collection_name=db_collection_name,
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port
        )

    @property
    def logtail_token(self) -> Optional[LogtailConnectionConfig]:
        """Propiedad para acceder al token de Logtail."""
        return self._logtail_token
        
    @logtail_token.setter
    def set_logtail_token(self, token: str) -> None:
        """Método para actualizar la configuración de Logtail."""
        self._logtail_token = token
        logging.info("Configuración de Logtail actualizada correctamente.")
    
    @property
    def teams_conn_config(self) -> Optional[TeamsConnectionConfig]:
        """Propiedad para acceder a la configuración de Teams."""
        return self._teams_conn_config

    def set_teams_conn_config(self, webhook: str, proyecto: str, pipeline: str, notify_to: List[str]) -> None:
        """Configura la conexión a Microsoft Teams."""
        self._teams_conn_config = TeamsConnectionConfig(
            webhook=webhook,
            proyecto=proyecto,
            pipeline=pipeline,
            notify_to=notify_to
        )