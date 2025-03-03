from typing import Dict, Tuple, Callable, List, Any
from base.Register import Register
from base.Ram import Ram


class ControlUnit:
    def __init__(
        self,
        memory: Ram,
        # Format: {opcode: (mnemonic, method, number_of_operands)}
        instruction_set: Dict[int, Tuple[str, Callable, int]],
        # Format {code: register}
        register_set: Dict[int, Tuple[str, Register]],
        # Format {code: (type, operand_size_byte)}
        operand_type_set: Dict[int, Tuple[str, int]],
    ):
        self.__memory: Ram = memory
        self.__register_set: Dict[int, Tuple[str, Register]] = register_set
        self.__R4: Register = self.__register_set[0x04][1]
        self.__R5: Register = self.__register_set[0x05][1]
        self.__instruction_set: Dict[int, Tuple[str, Callable, int]] = instruction_set
        self.__operand_type_set: Dict[int, Tuple[str, int]] = operand_type_set

    def __load_to_mbr(self):
        data: int = self.__memory.get_with_address(
            self.__R5.get(), len(self.__R4.value)
        )
        self.__R4.set(data)

    def __increment_pc(self):
        self.__R5.set(self.__R5.get() + 1)

    def __get_register_operand(self) -> Register:
        self.__increment_pc()
        self.__load_to_mbr()
        register_code = self.__R4.get()
        if register_code not in self.__register_set:
            raise ValueError(f"Unknown register code: {register_code}")
        return self.__register_set[register_code][1]

    def __get_value_operand(self) -> int:
        self.__increment_pc()
        self.__load_to_mbr()
        value = self.__memory.get_with_address(
            self.__R5.get(), self.__operand_type_set[0x01][1]
        )
        for _ in range(self.__operand_type_set[0x01][1]):
            self.__increment_pc()
        return value

    def __get_label_operand(self) -> str:
        self.__increment_pc()
        self.__load_to_mbr()
        label: str = (
            self.__memory.get_with_address(
                self.__R5.get(), self.__operand_type_set[0x02][1]
            )
            .to_bytes(
                self.__operand_type_set[0x02][1], byteorder="big"
            )  # Convert to bytes using big-endian byte order
            .decode("ascii")  # Convert to string
        )
        self.__increment_pc()  # Skip second byte of the operand (already read)
        return label

    def __get_operands(self, number_of_operands: int) -> List[Any]:
        operands = []
        # Get the last operand type
        self.__increment_pc()
        self.__load_to_mbr()
        last_operand_type_code = self.__R4.get()

        # For each operand except (-1) the last one (handle them as register)
        for i in range(number_of_operands - 1):
            operands.append(self.__get_register_operand())

        # Handle the last operand based on its type
        if last_operand_type_code not in self.__operand_type_set:
            raise ValueError(f"Unknown operand type code: {last_operand_type_code}")
        if last_operand_type_code == 0x00:  # Register
            operands.append(self.__get_register_operand())
            self.__increment_pc()
        elif last_operand_type_code == 0x01:
            operands.append(self.__get_value_operand())
        elif last_operand_type_code == 0x02:
            operands.append(self.__get_label_operand())
        return operands

    # Returns a tuple with the instruction and its operands
    def __decode_instruction(self) -> Tuple[Callable, List[Any]]:
        # Instruction format: [opcode (1 byte), [last_operand_type (1 byte), operand_1 ... operand_n (operand_type_set[last_operand_type][1] bytes)]]
        # Operands that are not the last one are always registers
        opcode = self.__R4.get()

        if opcode not in self.__instruction_set:
            raise ValueError(f"Unknown opcode: {opcode}")

        number_of_operands = self.__instruction_set[opcode][2]
        operands = []
        if number_of_operands > 0:
            operands = self.__get_operands(number_of_operands)
        return self.__instruction_set[opcode][1], operands

    def __execute_instruction(self, instruction: Tuple[Callable, List[Any]]):
        method: Callable = instruction[0]
        operands: List[Any] = instruction[1]
        try:
            method(*operands)
        except StopIteration as e:
            raise e

    def set_program_counter(self, address: int):
        self.__R5.set(address)

    def clock(self):
        # Fetch
        self.__load_to_mbr()
        instruction: Tuple[Callable, List[Any]] = self.__decode_instruction()
        # Execute
        try:
            self.__execute_instruction(instruction)
        except StopIteration as e:
            raise e
