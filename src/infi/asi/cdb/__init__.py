from infi.instruct import *

class CDB(Struct):
    _fields_ = []
    
    def create_datagram(self):
        return type(self).instance_to_string(self)

    def execute(self, executer):
        raise NotImplementedError()
