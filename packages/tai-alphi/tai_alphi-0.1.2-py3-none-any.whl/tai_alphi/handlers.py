import sys
import base64
import collections
import atexit
import paramiko
from io import StringIO
from logging import Handler, LogRecord, StreamHandler, INFO
from pymongo import MongoClient, errors
from datetime import datetime, timezone, timedelta


class ConsoleHandler(StreamHandler):

    def __init__(self):
        super().__init__(sys.stdout)
    
    def emit(self, record: LogRecord) -> None:
        return super().emit(record)


class CosmosHandler(Handler):
    
    def __init__(
            self,
            db_name: str,
            db_collection_name: str,
            db_user: str,
            db_password: str,
            db_host: str,
            db_port: int=10255,
            level=INFO,
        ) -> None:

        super().__init__(level)
        
        try:
            # Intentar conectar al cliente MongoDB
            client = MongoClient(
                host=db_host,
                port=db_port,
                tls=True,
                retrywrites=False,
                username=db_user,
                password=db_password,
                connectTimeoutMS=10000,
                serverSelectionTimeoutMS=10000, 
                socketTimeoutMS=10000
            )
            
            # Probar la conexión ejecutando un comando simple
            client.admin.command('ping')

            # Intentar acceder a la base de datos y la colección
            self.db = client[db_name]
            self.collection = self.db.get_collection(db_collection_name)
            self.indexes = self.collection.index_information()

            # Registrar el cierre del cliente al salir
            atexit.register(client.close)
            print("Conexión a MongoDB exitosa")

        except errors.ServerSelectionTimeoutError as e:
            print(f"Error de tiempo de espera al seleccionar el servidor de MongoDB: {e}")
            raise e
        except errors.OperationFailure as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise e
        except errors.ConnectionFailure as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise e
        except errors.ConfigurationError as e:
            print(f"Error de configuración en MongoDB: {e}")
            raise e
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
            raise e

    def emit(self, record: LogRecord):
        document = self.format(record)

        if 'expireAt_1' not in self.indexes:             
            self.collection.create_index("expireAt", expireAfterSeconds=0)

        utc_timestamp = datetime.now(timezone.utc)
        document["expireAt"] = utc_timestamp + timedelta(seconds=300)

        self.collection.insert_one(document)

class TeamsHandler(Handler):

    def __init__(self, level=INFO) -> None:
        super().__init__(level)
        self.queue = collections.deque(maxlen=500)

    def emit(self, record: LogRecord) -> None:
        self.queue.append(self.format(record))
    
    def get_queue(self):
        return self.queue
    
    def get_queue_contents(self):
        return "\n".join(self.queue)