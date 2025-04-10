from collections.abc import Callable
from dataclasses import dataclass
from base.Register import Register

type Byte = int

# Registers
type RegisterCode = Byte
type RegisterSet = dict[RegisterCode, Register]


# Instructions
@dataclass
class Instruction:
    mnemonic: str
    method: Callable
    number_of_operands: int


type Opcode = Byte
type InstructionSet = dict[Opcode, Instruction]


# Operand types
@dataclass
class OperandType:
    name: str
    operand_size_byte: int


type OperandTypeCode = Byte
type OperandTypeSet = dict[OperandTypeCode, OperandType]


# Interrupts
@dataclass
class Interrupt:
    interrupt_command: Byte
    memory_address: Byte
    arguments: bytearray
