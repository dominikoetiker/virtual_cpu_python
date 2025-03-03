class PcMemory:
    """Memory class for the PC. It stores the memory, labels, and the used memory.

    Attributes:
        memory (bytearray): Memory of the computer.
        is_used (list[bool]): List of booleans to check if the memory is used.
        labels (dict[str, int]): Dictionary of labels and their address pointers.
    """

    def __init__(self, memory_size_byte: int):
        """Initialize the memory with the size of the memory.

        Args:
            memory_size_byte (int): Size of the memory in bytes.
        """
        self.memory: bytearray = bytearray(memory_size_byte)
        self.is_used: list[bool] = [False] * memory_size_byte
        self.labels: dict[str, int] = {}  # label_name, address_pointer

    def __set(self, address: int, data_array: bytearray):
        """Set the data in the memory at the given address.

        Args:
            address (int): Address to set the data.
            data_array (bytearray): Data to set in the memory.

        Raises:
            ValueError: If the address is out of bounds.
            ValueError: If the data is out of bounds.
        """
        if address < 0 or address >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        if address + len(data_array) > len(self.memory):
            raise ValueError(f"Data {data_array} is out of bounds")
        for i in range(len(data_array)):
            self.memory[address + i] = data_array[i]
            self.is_used[address + i] = True

    @staticmethod
    def __convert_int_to_bytearray(data: int) -> bytearray:
        """Convert an integer to a bytearray.
        Follow the little-endian format.

        Args:
            data (int): Integer to convert to a bytearray.

        Returns:
            bytearray: Bytearray representation of the integer.
        """
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
        """Get the first address with enough free memory.

        Args:
            size (int): Size of the memory to get.

        Returns:
            int: Address with enough free memory.

        Raises:
            ValueError: If no free memory is available.
        """
        for i in range(len(self.memory) - size):
            if not any(self.is_used[i : i + size]):
                return i
        raise ValueError("No free memory available")

    def get_with_address(self, address: int, register_size: int) -> int:
        """Get the data from the memory at the given address.

        Args:
            address (int): Address to get the data.
            register_size (int): Size of the register, the value is going to be used at, in bytes.

        Returns:
            int: Data at the address.

        Raises:
            ValueError: If the address is out of bounds.
        """
        if address < 0 or address + register_size >= len(self.memory):
            raise ValueError(f"Address {address} is out of bounds")
        result = 0
        for i in range(register_size):
            # Shift data left by 8 bits (1 byte) and add the next byte
            result += self.memory[address + i] << (8 * i)
        return result

    def get_with_label(self, label: str, register_size: int) -> int:
        """Get the data from the memory at the given label.

        Args:
            label (str): Label to get the data.
            register_size (int): Size of the register, the value is going to be used at, in bytes.

        Returns:
            int: Data at the label.

        Raises:
            ValueError: If the label is not found.
        """
        if label in self.labels:
            return self.get_with_address(self.labels[label], register_size)
        raise ValueError(f"Label {label} not found")

    def set_with_address(self, address: int, data: int):
        """Set the data in the memory at the given address.

        Args:
            address (int): Address to set the data.
            data (int): Data to set in the memory.
        """
        data_array: bytearray = self.__convert_int_to_bytearray(data)
        self.__set(address, data_array)

    def set_with_label(self, label: str, data: int):
        """Set the data in the memory at the given label.

        Args:
            label (str): Label to set the data.
            data (int): Data to set in the memory.
        """
        data_array: bytearray = self.__convert_int_to_bytearray(data)
        if label in self.labels:
            self.__set(self.labels[label], data_array)
            return
        address: int = self.__get_free_memory(len(data_array))
        self.labels[label] = address
        self.__set(address, data_array)
