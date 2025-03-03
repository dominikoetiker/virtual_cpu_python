from typing import Union
from pc_memory import PcMemory
from register import Register

class Cpu():
    def __init__(self):
        self.memory: PcMemory = PcMemory(1024)
        self.R0: Register = Register(2) # General purpose register. Entry for A-Bus of ALU.
        self.R1: Register = Register(2) # General purpose register.
        self.R2: Register = Register(2) # OUT: Output register.
        self.R3: Register = Register(2) # LINK: Link register. Used internally by the CPU for jumps.
        self.R4: Register = Register(2) # MBR: Memory Byte Register. Data value (first byte) the Program Counter is pointing to.
        self.R5: Register = Register(2) # PC: Program Counter. Points to the next instruction to be executed
    
    def __register_to_int(self, register: Register) -> int:
        """
        Convert a register (bytearray) to an integer following the little-endian format.
        """
        result = 0
        for i in range(len(register.value)):
            result += register.get(i) << (8 * i)
        return result
    
    def __int_to_register(self, value: int, register: Register):
        """
        Convert an integer to a register (bytearray) following the little-endian format.
        """
        for i in range(len(register.value)):
            register.set(i, (value >> (8 * i)) & 0xFF)

    def asm_ADD(self, to_register: Register, summand1: Register, summand2: Union[Register, int]):
        if isinstance(summand2, Register):
            summand2 = self.__register_to_int(summand2)
        result = self.__register_to_int(summand1) + summand2
        self.__int_to_register(result, to_register)

    def asm_MOV(self, to_register: Register, value: Union[Register, int]):
        if isinstance(value, Register):
            value = self.__register_to_int(value)
        self.__int_to_register(value, to_register)

    def asm_LDR(self, to_register: Register, address: Union[str, Register]):
        pass

    def asm_STR(self, from_register: Register, address: Union[str, Register]):
        if isinstance(address, str):
            self.memory.set_with_label(address, self.__register_to_int(from_register))
        else:
            self.memory.set_with_address(address, self.__register_to_int(from_register))

    def asm_OUT(self, register: Register):
        self.R2 = register
        print(f"OUT: {self.__register_to_int(register)}")

    def asm_NOP(self):
        pass