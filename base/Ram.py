from typing import Union

from data_types import Byte


class Ram:

    def __init__(self, memory_size_byte: int):
        self.memory: bytearray = bytearray(memory_size_byte)

    def __set(self, address: int, data: bytearray) -> None:
        if address < 0 or address >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        if address + len(data) > len(self.memory):
            raise ValueError(f"Data {data} is out of bounds")
        for i in range(len(data)):
            self.memory[address + i] = data[i]

    def __convert_int_to_bytearray(self, data: int) -> bytearray:
        if data <= 0xFF:  # If the data fits in a byte, return it
            return bytearray([data])
        result: bytearray = bytearray()
        while data > 0:
            # Extract the least significant byte and add it to the result
            byte: Byte = data & 0xFF
            result.append(byte)
            # Shift data right by 8 bits (1 byte)
            data >>= 8
        return result

    def get_with_address(self, address: int, register_size: int) -> int:
        if address < 0 or address + register_size >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        result: int = 0
        for i in range(register_size):
            # Shift data left by 8 bits (1 byte) per position in register_size and add the next byte
            result += self.memory[address + i] << (8 * i)
        return result

    def set_with_address(self, address: int, data: Union[int, bytearray]) -> None:
        if isinstance(data, bytearray):
            data_array: bytearray = data
        else:
            data_array = self.__convert_int_to_bytearray(data)
        self.__set(address, data_array)
