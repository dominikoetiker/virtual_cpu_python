from typing import List, Dict, Union


class Ram:

    def __init__(self, memory_size_byte: int):
        self.memory: bytearray = bytearray(memory_size_byte)
        self.is_used: List[bool] = [False] * memory_size_byte
        self.labels: Dict[str, int] = {}  # label_name, address_pointer

    def __set(self, address: int, data_array: bytearray):
        if address < 0 or address >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        if address + len(data_array) > len(self.memory):
            raise ValueError(f"Data {data_array} is out of bounds")
        for i in range(len(data_array)):
            self.memory[address + i] = data_array[i]
            self.is_used[address + i] = True

    @staticmethod
    def __convert_int_to_bytearray(data: int) -> bytearray:
        if data <= 0xFF:  # If the data fits in a byte, return it
            return bytearray([data])
        result = bytearray()
        while data > 0:
            # Extract the least significant byte and add it to the result
            byte = data & 0xFF
            result.append(byte)
            # Shift data right by 8 bits (1 byte)
            data >>= 8
        return result

    def __get_free_memory(self, size: int) -> int:
        for i in range(len(self.memory) - size):
            if not any(self.is_used[i : i + size]):
                return i
        raise ValueError("No free memory available")

    def get_with_address(self, address: int, register_size: int) -> int:
        if address < 0 or address + register_size >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        result = 0
        for i in range(register_size):
            # Shift data left by 8 bits (1 byte) and add the next byte
            result += self.memory[address + i] << (8 * i)
        return result

    def get_with_label(self, label: str, register_size: int) -> int:
        if label in self.labels:
            return self.get_with_address(self.labels[label], register_size)
        raise ValueError(f"Label {label} not found")

    def set_with_address(self, address: int, data: Union[int, bytearray]):
        if isinstance(data, bytearray):
            data_array: bytearray = data
        else:
            data_array: bytearray = self.__convert_int_to_bytearray(data)
        self.__set(address, data_array)

    def set_with_label(self, label: str, data: Union[int, bytearray]):
        if isinstance(data, bytearray):
            data_array: bytearray = data
        else:
            data_array: bytearray = self.__convert_int_to_bytearray(data)
        if label in self.labels:
            self.__set(self.labels[label], data_array)
            return
        address: int = self.__get_free_memory(len(data_array))
        self.labels[label] = address
        self.__set(address, data_array)
