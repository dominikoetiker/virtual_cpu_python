from typing import Union
from base.Flag import Flag
from base.Register import Register
from base.Ram import Ram


class MemoryController:
    def __init__(self, zero_flag: Flag, memory: Ram):
        self.memory: Ram = memory
        self.Z: Flag = zero_flag

    def asm_LDR(self, to_register: Register, address: Union[str, Register]):
        if isinstance(address, str):
            data: int = self.memory.get_with_label(address, len(to_register.value))
        else:
            data: int = self.memory.get_with_address(
                address.get(), len(to_register.value)
            )
        to_register.set(data)

    def asm_STR(self, from_register: Register, address: Union[str, Register]):
        if isinstance(address, str):
            self.memory.set_with_label(address, from_register.get())
        else:
            self.memory.set_with_address(
                address.get(),
                from_register.get(),
            )
