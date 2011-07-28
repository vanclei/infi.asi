from . import CDB
from .. import SCSIReadCommand
from .operation_code import OperationCode
from .control import Control, DEFAULT_CONTROL
from infi.instruct import *
from ..errors import AsiException
# spc4r30: 6.4.1 (page 259)

CDB_OPCODE_READ_6 = 0x08
CDB_OPCODE_READ_10 = 0x28
CDB_OPCODE_READ_12 = 0xa8
CDB_OPCODE_READ_16 = 0x88

# TODO move this
DEFAULT_BLOCK_SIZE = 512

class Read6Command(CDB):
    _fields_ = [
        ConstField("opcode", OperationCode(opcode=CDB_OPCODE_READ_6)),
        BitFields(
            BitField("logical_block_address__msb", 5),
            BitPadding(3),
            ),
        UBInt16("logical_block_address__lsb"),
        UBInt8("transfer_length"),
        Field("control", Control, DEFAULT_CONTROL)
    ]

    def __init__(self, logical_block_address, block_size=DEFAULT_BLOCK_SIZE):
        super(Read6Command, self).__init__()
        self.logical_block_address = logical_block_address
        self.block_size = block_size

    def execute(self, executer):
        assert self.logical_block_address < 2 ** 21
        assert self.transfer_length < 2 ** 8

        self.logical_block_address__msb = self.logical_block_address >> 16
        self.logical_block_address__lsb = self.logical_block_address & 0xffff

        datagram = self.create_datagram()

        result_datagram = yield executer.call(SCSIReadCommand(datagram, self.block_size * self.transfer_length))

        yield result_datagram

class Read10Command(CDB):
    _fields_ = [
                ConstField("opcode", OperationCode(opcode=CDB_OPCODE_READ_10)),
                BitFields(
                          BitPadding(1),
                          Flag("fua_nv", 0),
                          BitPadding(1),
                          Flag("fua", 0),
                          Flag("dpo", 0),
                          BitField("rdprotect", 3, 0),
                          ),
                UBInt32("logical_block_address"),
                BitFields(
                          BitField("group_number", 5, 0),
                          BitPadding(3)),
                UBInt16("transfer_length"),
                Field("control", Control, DEFAULT_CONTROL)
                ]

    def __init__(self, block_size=DEFAULT_BLOCK_SIZE):
        super(Read10Command, self).__init__()
        self.block_size = block_size

    def execute(self, executer):
        assert self.logical_block_address < 2 ** 32
        assert self.transfer_length < 2 ** 16
        datagram = self.create_datagram()
        result_datagram = yield executer.call(SCSIReadCommand(datagram, self.block_size * self.transfer_length))

        yield result_datagram