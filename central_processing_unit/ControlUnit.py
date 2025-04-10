from typing import Tuple, Callable, List, Any
from base.Register import Register
from base.Ram import Ram
from data_types import InstructionSet, OperandTypeSet, RegisterSet


class ControlUnit:
    def __init__(
        self,
        memory: Ram,
        instruction_set: InstructionSet,
        register_set: RegisterSet,
        operand_type_set: OperandTypeSet,
    ):
        self.__memory: Ram = memory
        self.__register_set: RegisterSet = register_set
        self.__R4: Register = self.__register_set[0x04]
        self.__R5: Register = self.__register_set[0x05]
        self.__instruction_set: InstructionSet = instruction_set
        self.__operand_type_set: OperandTypeSet = operand_type_set

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
        return self.__register_set[register_code]

    def __get_value_operand(self) -> int:
        self.__increment_pc()
        self.__load_to_mbr()
        value = self.__memory.get_with_address(
            self.__R5.get(), self.__operand_type_set[0x01].operand_size_byte
        )
        for _ in range(self.__operand_type_set[0x01].operand_size_byte):
            self.__increment_pc()
        return value

    def __get_operands(self, number_of_operands: int) -> List[Any]:
        operands = []
        # Get the last operand type
        self.__increment_pc()
        self.__load_to_mbr()
        last_operand_type_code = self.__R4.get()

        # For each operand except (-1) the last one (handle them as register)
        for _ in range(number_of_operands - 1):
            operands.append(self.__get_register_operand())

        # Handle the last operand based on its type
        if last_operand_type_code not in self.__operand_type_set:
            raise ValueError(f"Unknown operand type code: {last_operand_type_code}")
        if last_operand_type_code == 0x00:  # Register
            operands.append(self.__get_register_operand())
            self.__increment_pc()
        elif last_operand_type_code == 0x01:  # Value
            operands.append(self.__get_value_operand())
        return operands

    # Returns a tuple with the instruction and its operands
    def __decode_instruction(self) -> Tuple[Callable, List[Any]]:
        # Instruction format: [opcode (1 byte), [last_operand_type (1 byte), operand_1 ... operand_n (operand_type_set[last_operand_type][1] bytes)]]
        # Operands that are not the last one are always registers
        opcode = self.__R4.get()

        if opcode not in self.__instruction_set:
            raise ValueError(f"Unknown opcode: {opcode}")

        number_of_operands = self.__instruction_set[opcode].number_of_operands
        operands = []
        if number_of_operands > 0:
            operands = self.__get_operands(number_of_operands)
        return self.__instruction_set[opcode].method, operands

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
        # Decode
        instruction: Tuple[Callable, List[Any]] = self.__decode_instruction()
        # Execute
        try:
            self.__execute_instruction(instruction)
        except StopIteration as e:
            raise e
