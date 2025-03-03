class Register:
    def __init__(self, register_size_byte: int):
        self.value: bytearray = bytearray(register_size_byte)
    
    def set(self, address: int, data: int):
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        if data < 0 or data > 0xFF:
            raise ValueError(f"Data {data} is out of bounds")
        self.value[address] = data
    
    def get(self, address: int) -> int:
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        return self.value[address]