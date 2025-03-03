class PcMemory:
    def __init__(self, memory_size_byte: int):
        self.memory: bytearray = bytearray(memory_size_byte)

    def set(self, address: int, data: int):
        if address < 0 or address >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        if data < 0 or data > 0xFF:
            raise ValueError(f"Data {data} is out of bounds")
        self.memory[address] = data
    
    def get(self, address: int) -> int:
        if address < 0 or address >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        return self.memory[address]