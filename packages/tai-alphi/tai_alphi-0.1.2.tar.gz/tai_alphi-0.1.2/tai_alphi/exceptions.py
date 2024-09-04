import sys

class Exitter:
    def __init__(self, msg) -> None:
        print(f"{self.__class__.__name__} : {msg}")
        sys.exit()

class ConfigFileError(Exitter):
    pass

class MissingConfig(Exitter):
    pass

class TypeError(Exitter):
    pass

class LogtailMissingToken(Exitter):
    def __init__(self) -> None:
        msg = '''
        No se ha encontrado el token para logtail.
        Considera: set_logtail_token
        o eliminar [logtail] del config file
        ''' 
        super().__init__(msg)

class VirtualMachineMissingConfig(Exitter):
    def __init__(self, missing_param) -> None:
        
        msg = f'''
        El parámetro {missing_param} es obligado
        Considera: set_vm_config
        o eliminar [nosqlDB] del config file
        '''
        super().__init__(msg)

class NosqlDBMissingConfig(Exitter):
    def __init__(self, missing_param) -> None:
        
        msg = f'''
        El parámetro {missing_param} es obligado
        Considera: set_nosqlDB_config
        o eliminar [nosqlDB] del config file
        '''
        super().__init__(msg)
    