class Register:
    def __init__(self, size_byte: int, name: str):
        self.value: bytearray = bytearray(size_byte)
        self.name: str = name

    def __set_byte_at_register_address(self, byte_position: int, data: int) -> None:
        if data < 0 or data > 0xFF:
            raise ValueError(f"Data {data} is out of bounds")
        self.value[byte_position] = data

    def __get_byte_from_register_address(self, byte_position: int) -> int:
        return self.value[byte_position]

    def get(self) -> int:
        result: int = 0
        for i in range(len(self.value)):
            result += self.__get_byte_from_register_address(i) << (8 * i)
        return result

    def set(self, value: int) -> None:
        for i in range(len(self.value)):
            self.__set_byte_at_register_address(i, (value >> (8 * i)) & 0xFF)
