class Register:
    """Register class to store values.

    Attributes:
        value (bytearray): Value of the register.
    """

    def __init__(self, register_size_byte: int):
        """Initialize the Register.

        Args:
            register_size_byte (int): Size of the register in bytes.
        """
        self.value: bytearray = bytearray(register_size_byte)

    def set(self, address: int, data: int):
        """Set the data in the register at the given address.

        Args:
            address (int): Address to set the data.
            data (int): Data to set in the register.

        Raises:
            ValueError: If the address is out of bounds.
            ValueError: If the data is out of bounds.
        """
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        if data < 0 or data > 0xFF:
            raise ValueError(f"Data {data} is out of bounds")
        self.value[address] = data

    def get(self, address: int) -> int:
        """Get the data from the register at the given address.

        Args:
            address (int): Address to get the data.

        Returns:
            int: Data at the address.

        Raises:
            ValueError: If the address is out of bounds.
        """
        if address < 0 or address >= len(self.value):
            raise ValueError(f"Address {address} is out of bounds")
        return self.value[address]
