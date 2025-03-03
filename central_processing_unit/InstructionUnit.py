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

    def asm_MOV(self, to_register: Register, value: Union[Register, int]):
        if isinstance(value, Register):
            value: int = value.get()
        to_register.set(value)

    def asm_BEQ(self, label: str):
        if self.Z.isFlagSet:
            address: int = self.memory.get_with_label(label, len(self.R5.value))
            self.R5.set(address)

    def asm_BNE(self, label: str):
        if not self.Z.isFlagSet:
            address: int = self.memory.get_with_label(label, len(self.R5.value))
            self.R5.set(address)

    def asm_B(self, label: str):
        address: int = self.memory.get_with_label(label, len(self.R5.value))
        self.R5.set(address)

    def asm_BL(self, label: str):
        self.R3.set(self.R5.get())
        address: int = self.memory.get_with_label(label, len(self.R5.value))
        self.R5.set(address)

    def asm_BX(self):
        self.R5.set(self.R3.get())

    def asm_HLT(self):
        raise StopIteration("HLT instruction executed")

    def asm_NOP(self):
        pass
