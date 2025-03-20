from central_processing_unit.ArithmeticLogicUnit import ArithmeticLogicUnit
from typing import Union, Dict, Tuple
from base.Register import Register
from base.Flag import Flag
from base.Ram import Ram


class InstructionUnit:
    def __init__(
        self,
        zero_flag: Flag,
        memory: Ram,
        register_set: Dict[int, Tuple[str, Register]],
    ):
        self.Z: Flag = zero_flag
        self.memory: Ram = memory
        self.R3: Register = register_set[0x03][1]
        self.R5: Register = register_set[0x05][1]
        self.R6: Register = register_set[0x06][1]

    def __jump_to_address(self, address: Union[Register, int]):
        if isinstance(address, Register):
            address = address.get()
        self.R5.set(address)

    def __add_current_program_start_address(self, address: Union[Register, int]) -> int:
        if isinstance(address, Register):
            address = address.get()
        print(f"DEBUG from __add_current_program_start_address address = {address}")
        print(f"DEBUG from __add_current_program_start_address R6 = {self.R6.get()}")
        return address + self.R6.get()

    def asm_MOV(self, to_register: Register, value: Union[Register, int]):
        if isinstance(value, Register):
            value = value.get()
        to_register.set(value)

    def asm_BEQ(self, address: Union[Register, int]):
        if self.Z.isFlagSet:
            address = self.__add_current_program_start_address(address)
            self.__jump_to_address(address)

    def asm_BNE(self, address: Union[Register, int]):
        if not self.Z.isFlagSet:
            address = self.__add_current_program_start_address(address)
            self.__jump_to_address(address)

    def asm_B(self, address: Union[Register, int]):
        print(f"DEBUG from asm_B address before adding R6 = {address}")
        address = self.__add_current_program_start_address(address)
        print(f"DEBUG from asm_B address after adding R6 = {address}")
        self.__jump_to_address(address)

    def asm_BL(self, address: Union[Register, int]):
        print(f"DEBUG from asm_BL address = {address}")
        self.R3.set(self.R5.get())
        print(f"DEBUG from asm_BL R3 = {self.R3.get()}")
        print(f"DEBUG from asm_BL R5 = {self.R5.get()}")
        self.__jump_to_address(address)

    def asm_BX(self):
        print(f"DEBUG from asm_BX R3 = {self.R3.get()}")
        self.__jump_to_address(self.R3)

    def asm_HLT(self):
        raise StopIteration("HLT instruction executed")

    def asm_NOP(self):
        pass
