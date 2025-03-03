from typing import Union
from pc_memory import PcMemory
from register import Register


class Cpu:
    """CPU class that contains the registers and the memory of the computer.

    Attributes:
        memory (PcMemory): Memory of the computer.
        R0 (Register): General purpose register. Entry for A-Bus of ALU.
        R1 (Register): General purpose register.
        R2 (Register): OUT: Output register.
        R3 (Register): LINK: Link register. Used internally by the CPU for jumps.
        R4 (Register): MBR: Memory Byte Register. Data value (first byte) the Program Counter is pointing to.
        R5 (Register): PC: Program Counter. Points to the next instruction to be executed
        Z (bool): Zero flag. Set if the result of an operation is zero.
    """

    def __init__(
        self,
        memory_size_byte: int = 1024,
        r0_size_byte: int = 2,
        r1_size_byte: int = 2,
        r2_size_byte: int = 2,
        r3_size_byte: int = 2,
        r4_size_byte: int = 2,
        r5_size_byte: int = 2,
    ):
        """Initialize the CPU with the registers and memory.

        Args:
            memory_size_byte (int, optional): Size of the memory in bytes. Defaults to 1024.
            r0_size_byte (int, optional): Size of the R0 register in bytes. Defaults to 2.
            r1_size_byte (int, optional): Size of the R1 register in bytes. Defaults to 2.
            r2_size_byte (int, optional): Size of the R2 register in bytes. Defaults to 2.
            r3_size_byte (int, optional): Size of the R3 register in bytes. Defaults to 2.
            r4_size_byte (int, optional): Size of the R4 register in bytes. Defaults to 2.
            r5_size_byte (int, optional): Size of the R5 register in bytes. Defaults to 2.
        """
        self.memory: PcMemory = PcMemory(memory_size_byte)
        self.R0: Register = Register(r0_size_byte)
        self.R1: Register = Register(r1_size_byte)
        self.R2: Register = Register(r2_size_byte)
        self.R3: Register = Register(r3_size_byte)
        self.R4: Register = Register(r4_size_byte)
        self.R5: Register = Register(r5_size_byte)
        self.Z: bool = False  # Zero flag

    def __register_to_int(self, register: Register) -> int:
        """Convert a register (bytearray) to an integer following the little-endian format.

        Args:
            register (Register): Register to convert to an integer.

        Returns:
            int: Integer representation of the register.
        """
        result: int = 0
        for i in range(len(register.value)):
            result += register.get(i) << (8 * i)
        return result

    def __int_to_register(self, value: int, register: Register):
        """Convert an integer to a register (bytearray) following the little-endian format.

        Args:
            value (int): Integer to convert to a register.
            register (Register): Register to store the integer.
        """
        for i in range(len(register.value)):
            register.set(i, (value >> (8 * i)) & 0xFF)

    def __set_zero_flag(self, value: int):
        """Set the zero flag if the value is zero.

        Args:
            value (int): Value to check if it is zero.
        """
        self.Z = value == 0

    def asm_ADD(
        self, to_register: Register, summand1: Register, summand2: Union[Register, int]
    ):
        """Add two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            summand1 (Register): Register with the first summand.
            summand2 (Union[Register, int]): Second summand from a Register or as a value.
        """
        if isinstance(summand2, Register):
            summand2: int = self.__register_to_int(summand2)
        result: int = self.__register_to_int(summand1) + summand2
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_SUB(
        self, to_register: Register, minuend: Register, subtrahend: Union[Register, int]
    ):
        """Subtract two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            minuend (Register): Register with the minuend.
            subtrahend (Union[Register, int]): Subtrahend from a Register or as a value.
        """
        if isinstance(subtrahend, Register):
            subtrahend: int = self.__register_to_int(subtrahend)
        result: int = self.__register_to_int(minuend) - subtrahend
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_MUL(
        self, to_register: Register, factor1: Register, factor2: Union[Register, int]
    ):
        """Multiply two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            factor1 (Register): Register with the first factor.
            factor2 (Union[Register, int]): Second factor from a Register or as a value.
        """
        if isinstance(factor2, Register):
            factor2: int = self.__register_to_int(factor2)
        result: int = self.__register_to_int(factor1) * factor2
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_DIV(
        self, to_register: Register, dividend: Register, divisor: Union[Register, int]
    ):
        """Divide two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            dividend (Register): Register with the dividend.
            divisor (Union[Register, int]): Divisor from a Register or as a value.
        """
        if isinstance(divisor, Register):
            divisor: int = self.__register_to_int(divisor)
        result: int = self.__register_to_int(dividend) // divisor  # Integer division
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_MOD(
        self, to_register: Register, dividend: Register, divisor: Union[Register, int]
    ):
        """Calculate the modulo of two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            dividend (Register): Register with the dividend.
            divisor (Union[Register, int]): Divisor from a Register or as a value.
        """
        if isinstance(divisor, Register):
            divisor: int = self.__register_to_int(divisor)
        result: int = self.__register_to_int(dividend) % divisor
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_AND(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        """Perform a bitwise AND operation between two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand1 (Register): Register with the first operand.
            operand2 (Union[Register, int]): Second operand from a Register or as a value.
        """
        if isinstance(operand2, Register):
            operand2: int = self.__register_to_int(operand2)
        result: int = self.__register_to_int(operand1) & operand2
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_ORR(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        """Perform a bitwise OR operation between two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand1 (Register): Register with the first operand.
            operand2 (Union[Register, int]): Second operand from a Register or as a value.
        """
        if isinstance(operand2, Register):
            operand2: int = self.__register_to_int(operand2)
        result: int = self.__register_to_int(operand1) | operand2
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_XOR(
        self, to_register: Register, operand1: Register, operand2: Union[Register, int]
    ):
        """Perform a bitwise XOR operation between two values and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand1 (Register): Register with the first operand.
            operand2 (Union[Register, int]): Second operand from a Register or as a value.
        """
        if isinstance(operand2, Register):
            operand2: int = self.__register_to_int(operand2)
        result: int = self.__register_to_int(operand1) ^ operand2
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_NOT(self, to_register: Register, operand: Union[Register, int]):
        """Perform a bitwise NOT operation on a value and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand (Union[Register, int]): Operand from a Register or as a value.
        """
        if isinstance(operand, Register):
            operand: int = self.__register_to_int(operand)
        result: int = ~operand
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_LSL(
        self, to_register: Register, operand: Register, shift: Union[Register, int]
    ):
        """Perform a logical shift left operation on a value and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand (Register): Register with the value to shift.
            shift (Union[Register, int]): Shift value from a Register or as a value.
        """
        if isinstance(shift, Register):
            shift: int = self.__register_to_int(shift)
        result: int = self.__register_to_int(operand) << shift
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_LSR(
        self, to_register: Register, operand: Register, shift: Union[Register, int]
    ):
        """Perform a logical shift right operation on a value and store the result in a register.

        Args:
            to_register (Register): Register to store the result.
            operand (Register): Register with the value to shift.
            shift (Union[Register, int]): Shift value from a Register or as a value.
        """
        if isinstance(shift, Register):
            shift: int = self.__register_to_int(shift)
        result: int = self.__register_to_int(operand) >> shift
        self.__set_zero_flag(result)
        self.__int_to_register(result, to_register)

    def asm_MOV(self, to_register: Register, value: Union[Register, int]):
        """Move a value to a register.

        Args:
            to_register (Register): Register to store the value.
            value (Union[Register, int]): Value to store in the register. If it is a Register, convert it to an integer.
        """
        if isinstance(value, Register):
            value: int = self.__register_to_int(value)
        self.__int_to_register(value, to_register)

    def asm_LDR(self, to_register: Register, address: Union[str, Register]):
        """Load a value from memory to a register.

        Args:
            to_register (Register): Register to store the value.
            address (Union[str, Register]): Address in memory to load the value. If it is a string, use it as a label.
        """
        if isinstance(address, str):
            data: int = self.memory.get_with_label(address, len(to_register.value))
        else:
            data: int = self.memory.get_with_address(
                self.__register_to_int(address), len(to_register.value)
            )
        self.__int_to_register(data, to_register)

    def asm_STR(self, from_register: Register, address: Union[str, Register]):
        """Store a value from a register to memory.

        Args:
            from_register (Register): Register with the value to store.
            address (Union[str, Register]): Address in memory to store the value. If it is a string, use it as a label.
        """
        if isinstance(address, str):
            self.memory.set_with_label(address, self.__register_to_int(from_register))
        else:
            self.memory.set_with_address(
                self.__register_to_int(address), self.__register_to_int(from_register)
            )

    def asm_CMP(self, operand1: Register, operand2: Union[Register, int]):
        """Compare two values and set the zero flag if they are equal.

        Args:
            operand1 (Register): Register with the first operand.
            operand2 (Union[Register, int]): Second operand from a Register or as a value.
        """
        if isinstance(operand2, Register):
            operand2: int = self.__register_to_int(operand2)
        self.Z = self.__register_to_int(operand1) == operand2

    def asm_BEQ(self, label: str):
        """Branch if the zero flag is set.

        Args:
            label (str): Label to jump to.
        """
        if self.Z:
            address: int = self.memory.get_with_label(label, len(self.R5.value))
            self.__int_to_register(address, self.R5)

    def asm_BNE(self, label: str):
        """Branch if the zero flag is not set.

        Args:
            label (str): Label to jump to.
        """
        if not self.Z:
            address: int = self.memory.get_with_label(label, len(self.R5.value))
            self.__int_to_register(address, self.R5)

    def asm_B(self, label: str):
        """Branch to a label.

        Args:
            label (str): Label to jump to.
        """
        address: int = self.memory.get_with_label(label, len(self.R5.value))
        self.__int_to_register(address, self.R5)

    def asm_BL(self, label: str):
        """Branch to a label and link the return address to jump back.

        Args:
            label (str): Label to jump to.
        """
        self.__int_to_register(self.__register_to_int(self.R5), self.R3)
        address: int = self.memory.get_with_label(label, len(self.R5.value))
        self.__int_to_register(address, self.R5)

    def asm_BX(self):
        """Branch to the link register. Jump back from a subroutine."""
        self.__int_to_register(self.__register_to_int(self.R3), self.R5)

    def asm_INP(self, register: Register):
        """Input a value to a register.

        Args:
            register (Register): Register to input the value.
        """
        text: str = input("INP: ")
        data: int = int.from_bytes(text.encode("ascii"), byteorder="big")
        self.__int_to_register(data, register)

    def asm_OUT(self, register: Register):
        """Output the value of a register.

        Args:
            register (Register): Register to output.
        """
        self.R2 = register
        print(f"OUT: {self.__register_to_int(register)}")

    def asm_HLT(self):
        """Halt the CPU. Stop the execution."""
        exit()

    def asm_NOP(self):
        """No operation. Do nothing"""
        pass
