from typing import Union
from base.Flag import Flag
from base.Register import Register


class ArithmeticLogicUnit:
    def __init__(self, zero_flag: Flag):
        self.Z: Flag = zero_flag

    # Arithmetic operations
    def asm_ADD(
        self, to_register: Register, summand1: Register, summand2: Union[Register, int]
    ):
        if isinstance(summand2, Register):
            summand2 = summand2.get()
        result: int = summand1.get() + summand2
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_SUB(
        self, to_register: Register, minuend: Register, subtrahend: Union[Register, int]
    ):
        if isinstance(subtrahend, Register):
            subtrahend = subtrahend.get()
        result: int = minuend.get() - subtrahend
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_MUL(
        self, to_register: Register, factor1: Register, factor2: Union[Register, int]
    ):
        if isinstance(factor2, Register):
            factor2 = factor2.get()
        result: int = factor1.get() * factor2
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_DIV(
        self, to_register: Register, dividend: Register, divisor: Union[Register, int]
    ):
        if isinstance(divisor, Register):
            divisor = divisor.get()
        result: int = dividend.get() // divisor  # Integer division
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_MOD(
        self, to_register: Register, dividend: Register, divisor: Union[Register, int]
    ):
        if isinstance(divisor, Register):
            divisor = divisor.get()
        result: int = dividend.get() % divisor
        to_register.set(result)
        self.Z.set_is_zero(result)

    # Logical operations
    def asm_AND(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        if isinstance(operand2, Register):
            operand2 = operand2.get()
        result: int = operand1.get() & operand2
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_ORR(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        if isinstance(operand2, Register):
            operand2 = operand2.get()
        result: int = operand1.get() | operand2
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_XOR(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        if isinstance(operand2, Register):
            operand2 = operand2.get()
        result: int = operand1.get() ^ operand2
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_NOT(self, to_register: Register, operand: Union[Register, int]):
        if isinstance(operand, Register):
            operand = operand.get()
        result: int = ~operand
        to_register.set(result)
        self.Z.set_is_zero(result)

    # Shift operations
    def asm_LSL(
        self, to_register: Register, operand: Register, shift: Union[Register, int]
    ):
        if isinstance(shift, Register):
            shift = shift.get()
        result: int = operand.get() << shift
        to_register.set(result)
        self.Z.set_is_zero(result)

    def asm_LSR(
        self, to_register: Register, operand: Register, shift: Union[Register, int]
    ):
        if isinstance(shift, Register):
            shift = shift.get()
        result: int = operand.get() >> shift
        to_register.set(result)
        self.Z.set_is_zero(result)

    # Compare operations
    def asm_CMP(self, operand1: Register, operand2: Union[Register, int]):
        if isinstance(operand2, Register):
            operand2 = operand2.get()
        result: int = operand1.get() - operand2
        self.Z.set_is_zero(result)
