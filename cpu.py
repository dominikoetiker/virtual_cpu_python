from typing import Union
from pc_memory import PcMemory
from register import Register

class Cpu():
    def __init__(self):
        self.memory: PcMemory = PcMemory(1024)
        self.R0: Register = Register(1) # General purpose register. Entry for A-Bus of ALU.
        self.R1: Register = Register(1) # General purpose register.
        self.R2: Register = Register(1) # OUT: Output register.
        self.R3: Register = Register(1) # LINK: Link register. Used internally by the CPU for jumps.
        self.R4: Register = Register(1) # MBR: Memory Byte Register. Data value (first byte) the Program Counter is pointing to.
        self.R5: Register = Register(1) # PC: Program Counter. Points to the next instruction to be executed
    
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
        Convert an integer to a register (bytearray) following the little-endian
        format.
        """
        for i in range(len(register.value)):
            register.set(i, (value >> (8 * i)) & 0xFF)

    def asm_NOP(self):
        pass

    def asm_STR(self, address: int, data: int):
        self.memory.set(address, data)

    def asm_LDR(self, address: int) -> int:
        return self.memory.get(address)

    def asm_ADD(self, to_register: Register, summand1: Register, summand2: Union[Register, int]):
        if isinstance(summand2, Register):
            summand2 = self.__register_to_int(summand2)
        result = self.__register_to_int(summand1) + summand2
        self.__int_to_register(result, to_register)