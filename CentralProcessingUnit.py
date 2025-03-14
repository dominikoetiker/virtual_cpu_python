from typing import Dict, Tuple, Callable
from base.Flag import Flag
from base.Ram import Ram
from base.Register import Register
from central_processing_unit.ArithmeticLogicUnit import ArithmeticLogicUnit
from central_processing_unit.ControlUnit import ControlUnit
from central_processing_unit.InstructionUnit import InstructionUnit
from IO_controller.IoController import IoController
from memory_controller.MemoryController import MemoryController


class CentralProcessingUnit:
    def __init__(
        self,
        memory_size_byte: int = 1024,
        r0_size_byte: int = 2,
        r1_size_byte: int = 2,
        r2_size_byte: int = 2,
        r3_size_byte: int = 2,
        r5_size_byte: int = 2,
    ):
        self.__Z: Flag = Flag()  # Zero flag
        self.__memory: Ram = Ram(memory_size_byte)
        self.__R0: Register = Register(r0_size_byte)  # General purpose register
        self.__R1: Register = Register(r1_size_byte)  # General purpose register
        self.__R2: Register = Register(r2_size_byte)  # Output register
        self.__R3: Register = Register(r3_size_byte)  # Link register
        self.__R4: Register = Register(1)  # Memory byte register only 1 byte
        self.__R5: Register = Register(r5_size_byte)  # Program counter
        # Format {code: (name, register)}
        self.__register_set: Dict[int, Tuple[str, Register]] = {
            0x00: ("R0", self.__R0),
            0x01: ("R1", self.__R1),
            0x02: ("R2", self.__R2),
            0x03: ("R3", self.__R3),
            0x04: ("R4", self.__R4),
            0x05: ("R5", self.__R5),
        }
        self.__arithmetic_logic_unit: ArithmeticLogicUnit = ArithmeticLogicUnit(
            self.__Z
        )
        self.__instruction_unit: InstructionUnit = InstructionUnit(
            self.__Z, self.__memory, self.__register_set
        )
        self.__io_controller: IoController = IoController(self.__register_set)
        self.__memory_controller: MemoryController = MemoryController(
            self.__Z, self.__memory
        )
        # Format: {opcode: (mnemonic, method, number_of_operands)}
        self.__instruction_set: Dict[int, Tuple[str, Callable, int]] = {
            # Control operations
            0x00: ("NOP", self.__instruction_unit.asm_NOP, 0),
            0x01: ("HLT", self.__instruction_unit.asm_HLT, 0),
            # Data operations
            0x02: ("MOV", self.__instruction_unit.asm_MOV, 2),
            # Branch operations
            0x03: ("BEQ", self.__instruction_unit.asm_BEQ, 1),
            0x04: ("BNE", self.__instruction_unit.asm_BNE, 1),
            0x05: ("B", self.__instruction_unit.asm_B, 1),
            0x06: ("BL", self.__instruction_unit.asm_BL, 1),
            0x07: ("BX", self.__instruction_unit.asm_BX, 0),
            # Arithmetic operations
            0x08: ("ADD", self.__arithmetic_logic_unit.asm_ADD, 3),
            0x09: ("SUB", self.__arithmetic_logic_unit.asm_SUB, 3),
            0x0A: ("MUL", self.__arithmetic_logic_unit.asm_MUL, 3),
            0x0B: ("DIV", self.__arithmetic_logic_unit.asm_DIV, 3),
            0x0C: ("MOD", self.__arithmetic_logic_unit.asm_MOD, 3),
            # Logical operations
            0x0D: ("AND", self.__arithmetic_logic_unit.asm_AND, 3),
            0x0E: ("ORR", self.__arithmetic_logic_unit.asm_ORR, 3),
            0x0F: ("XOR", self.__arithmetic_logic_unit.asm_XOR, 3),
            0x10: ("NOT", self.__arithmetic_logic_unit.asm_NOT, 2),
            # Shift operations
            0x11: ("LSL", self.__arithmetic_logic_unit.asm_LSL, 3),
            0x12: ("LSR", self.__arithmetic_logic_unit.asm_LSR, 3),
            # Compare operations
            0x13: ("CMP", self.__arithmetic_logic_unit.asm_CMP, 2),
            # Memory operations
            0x14: ("LDR", self.__memory_controller.asm_LDR, 2),
            0x15: ("STR", self.__memory_controller.asm_STR, 2),
            # I/O operations
            0x16: ("INP", self.__io_controller.asm_INP, 1),
            0x17: ("OUT", self.__io_controller.asm_OUT, 1),
            0x18: ("OUTC", self.__io_controller.asm_OUTC, 1),
        }
        # Format {code: (type, operand_size_byte)}
        self.__operand_type_set: Dict[int, Tuple[str, int]] = {
            0x00: ("register", 1),
            0x01: ("value", 2),
        }

        self.__control_unit: ControlUnit = ControlUnit(
            self.__memory,
            self.__instruction_set,
            self.__register_set,
            self.__operand_type_set,
        )

    def load_program(self, program: bytearray):
        self.__memory.set_with_address(0x00, program)

    def run(self):
        self.__control_unit.set_program_counter(0x00)
        try:
            while True:
                self.__control_unit.clock()
        except StopIteration as e:
            print(e)
            return
