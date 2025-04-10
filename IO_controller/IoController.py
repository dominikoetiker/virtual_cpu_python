from base.Register import Register
from data_types import RegisterSet


class IoController:
    def __init__(self, register_set: RegisterSet):
        self.R2 = register_set[0x02]

    def asm_INP(self, register: Register):
        text: str = input("INP: ")
        try:
            data: int = int(text)
        except ValueError:  # if the input is not an integer convert it to ascii
            data: int = int.from_bytes(text.encode("ascii"), byteorder="big")
        register.set(data)

    def asm_OUT(self, register: Register):
        self.R2.set(register.get())
        print(f"{register.get()}")

    def asm_OUTC(self, register: Register):
        self.R2.set(register.get())
        print(f"{chr(register.get())}", end="")
