from base.Register import Register
from typing import TypeAlias, NewType, Union
from collections.abc import Callable

# General
ByteValue: TypeAlias = int  # Integer Values in form of hexcoded bytes like 0x01, etc.

# Memory
MemoryAddress: TypeAlias = int  # Addresses like 0xA0, etc.

# Operands
OperandTypeCode: TypeAlias = int  # Codes like 0x00, 0x01, etc.
OperandTypeName: TypeAlias = str  # Names like "register" "value"
OperandSize: TypeAlias = int  # Size of the operand in bytes
OperandDefinition: TypeAlias = tuple[OperandTypeName, OperandSize]
OperandTypeSet: TypeAlias = dict[OperandTypeCode, OperandDefinition]

# Registers
RegisterCode: TypeAlias = int  # Codes like 0x00, 0x01, etc.
RegisterName: TypeAlias = str  # Names like "R1", "R2", etc.
NamedRegister: TypeAlias = tuple[RegisterName, Register]
RegisterSet: TypeAlias = dict[RegisterCode, NamedRegister]

# Instructions
Opcode: TypeAlias = int  # Opcodes like 0x00, 0x01, etc.
Mnemonic: TypeAlias = str  # Mnemonics like "ADD", "HLT", etc.
NumberOfOperands: TypeAlias = int
InstructionSet: TypeAlias = dict[Opcode, tuple[Mnemonic, Callable, NumberOfOperands]]

# Interrupts
ByteCodeProgram: TypeAlias = list[
    Union[Opcode, OperandTypeCode, RegisterCode, MemoryAddress, ByteValue]
]
Interrupt: TypeAlias = tuple[Opcode, MemoryAddress, ByteCodeProgram]
