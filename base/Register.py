class Register:
    def __init__(self, register_size_byte: int):
        self.value: bytearray = bytearray(register_size_byte)

    def __set_byte_at_register_address(self, address: int, data: int):
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        if data < 0 or data > 0xFF:
            raise ValueError(f"Data {data} is out of bounds")
        self.value[address] = data

    def __get_byte_from_register_address(self, address: int) -> int:
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        return self.value[address]

    def get(self) -> int:
        result: int = 0
        for i in range(len(self.value)):
            result += self.__get_byte_from_register_address(i) << (8 * i)
        return result

    def set(self, value: int):
        for i in range(len(self.value)):
            self.__set_byte_at_register_address(i, (value >> (8 * i)) & 0xFF)
