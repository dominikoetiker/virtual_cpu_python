from dataclasses import dataclass
from typing import Union, Protocol
from base.Register import Register

type Byte = int

# Registers
type RegisterCode = Byte
type RegisterSet = dict[RegisterCode, Register]


# Instructions
type Operand = Union[Register, int, None]
type Operands = list[Operand]


class Instruction_ZeroOperands(Protocol):
    def __call__(self) -> None:
        pass


class Instruction_OneOperand(Protocol):
    def __call__(self, first_operand: Operand) -> None:
        pass


class Instruction_TwoOperands(Protocol):
    def __call__(self, first_operand: Operand, second_operand: Operand) -> None:
        pass


class Instruction_ThreeOperands(Protocol):
    def __call__(
        self, first_operand: Operand, second_operand: Operand, third_operand: Operand
    ) -> None:
        pass


type InstructionMethod = Union[
    Instruction_ZeroOperands,
    Instruction_OneOperand,
    Instruction_TwoOperands,
    Instruction_ThreeOperands,
]


@dataclass
class MetaInstruction:
    mnemonic: str
    method: InstructionMethod
    number_of_operands: int


@dataclass
class Instruction:
    method: InstructionMethod
    operands: Operands


type Opcode = Byte
type InstructionSet = dict[Opcode, MetaInstruction]


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


# CPU context
@dataclass
class CPUContext:
    R0: int
    R1: int
    R2: int
    R3: int
    R4: int
    R5: int
    R6: int
