from typing import cast
from base.Flag import Flag
from base.Ram import Ram
from base.Register import Register
from central_processing_unit.ArithmeticLogicUnit import ArithmeticLogicUnit
from central_processing_unit.ControlUnit import ControlUnit
from central_processing_unit.InstructionUnit import InstructionUnit
from IO_controller.IoController import IoController
from memory_controller.MemoryController import MemoryController
from interrupt_controller.InterruptController import InterruptController
from data_types import Byte, Instruction_OneOperand, Instruction_ThreeOperands, Instruction_TwoOperands, Instruction_ZeroOperands, MetaInstruction, InstructionSet, Interrupt, OperandType, OperandTypeSet, RegisterSet


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
        self.__register_set: RegisterSet = {
            0x00: Register(size_byte=r0_size_byte, name="R0"),  # General purpose register # fmt: skip
            0x01: Register(size_byte=r1_size_byte, name="R1"),  # General purpose register # fmt: skip
            0x02: Register(size_byte=r2_size_byte, name="R2"),  # Output register # fmt: skip
            0x03: Register(size_byte=r3_size_byte, name="R3"),  # Link register # fmt: skip
            0x04: Register(size_byte=1,            name="R4"),  # Memory byte register only 1 byte # fmt: skip
            0x05: Register(size_byte=r5_size_byte, name="R5"),  # Program counter # fmt: skip
            0x06: Register(size_byte=r5_size_byte, name="R6"),  # Current program base address # fmt: skip
        }
        self.__arithmetic_logic_unit: ArithmeticLogicUnit = ArithmeticLogicUnit(self.__Z) # fmt: skip
        self.__instruction_unit: InstructionUnit          = InstructionUnit(self.__Z, self.__memory, self.__register_set) # fmt: skip
        self.__io_controller: IoController                = IoController(self.__register_set)
        self.__memory_controller: MemoryController        = MemoryController(self.__Z, self.__memory) # fmt: skip
        self.__interrupt_controller: InterruptController  = InterruptController(self.__register_set) # fmt: skip
        self.__instruction_set: InstructionSet = {
            # Control operations
            0x00: MetaInstruction(mnemonic="NOP",  method=cast(Instruction_ZeroOperands, self.__instruction_unit.asm_NOP),       number_of_operands=0), # fmt: skip
            0x01: MetaInstruction(mnemonic="HLT",  method=cast(Instruction_ZeroOperands, self.__instruction_unit.asm_HLT),       number_of_operands=0), # fmt: skip
            # Data operations
            0x02: MetaInstruction(mnemonic="MOV",  method=cast(Instruction_TwoOperands, self.__instruction_unit.asm_MOV),        number_of_operands=2), # fmt: skip
            # Branch operations
            0x03: MetaInstruction(mnemonic="BEQ",  method=cast(Instruction_OneOperand, self.__instruction_unit.asm_BEQ),         number_of_operands=1), # fmt: skip
            0x04: MetaInstruction(mnemonic="BNE",  method=cast(Instruction_OneOperand, self.__instruction_unit.asm_BNE),         number_of_operands=1), # fmt: skip
            0x05: MetaInstruction(mnemonic="B",    method=cast(Instruction_OneOperand, self.__instruction_unit.asm_B),           number_of_operands=1), # fmt: skip
            0x06: MetaInstruction(mnemonic="BL",   method=cast(Instruction_OneOperand, self.__instruction_unit.asm_BL),          number_of_operands=1), # fmt: skip
            0x07: MetaInstruction(mnemonic="BX",   method=cast(Instruction_ZeroOperands, self.__instruction_unit.asm_BX),        number_of_operands=0), # fmt: skip
            # Arithmetic operations
            0x08: MetaInstruction(mnemonic="ADD",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_ADD), number_of_operands=3), # fmt: skip
            0x09: MetaInstruction(mnemonic="SUB",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_SUB), number_of_operands=3), # fmt: skip
            0x0A: MetaInstruction(mnemonic="MUL",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_MUL), number_of_operands=3), # fmt: skip
            0x0B: MetaInstruction(mnemonic="DIV",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_DIV), number_of_operands=3), # fmt: skip
            0x0C: MetaInstruction(mnemonic="MOD",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_MOD), number_of_operands=3), # fmt: skip
            # Logical operations
            0x0D: MetaInstruction(mnemonic="AND",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_AND), number_of_operands=3), # fmt: skip
            0x0E: MetaInstruction(mnemonic="ORR",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_ORR), number_of_operands=3), # fmt: skip
            0x0F: MetaInstruction(mnemonic="XOR",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_XOR), number_of_operands=3), # fmt: skip
            0x10: MetaInstruction(mnemonic="NOT",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_NOT), number_of_operands=2), # fmt: skip
            # Shift operations
            0x11: MetaInstruction(mnemonic="LSL",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_LSL), number_of_operands=3), # fmt: skip
            0x12: MetaInstruction(mnemonic="LSR",  method=cast(Instruction_ThreeOperands, self.__arithmetic_logic_unit.asm_LSR), number_of_operands=3), # fmt: skip
            # Compare operations
            0x13: MetaInstruction(mnemonic="CMP",  method=cast(Instruction_TwoOperands, self.__arithmetic_logic_unit.asm_CMP),   number_of_operands=2), # fmt: skip
            # Memory operations
            0x14: MetaInstruction(mnemonic="LDR",  method=cast(Instruction_TwoOperands, self.__memory_controller.asm_LDR),       number_of_operands=2), # fmt: skip
            0x15: MetaInstruction(mnemonic="STR",  method=cast(Instruction_TwoOperands, self.__memory_controller.asm_STR),       number_of_operands=2), # fmt: skip
            # I/O operations
            0x16: MetaInstruction(mnemonic="INP",  method=cast(Instruction_OneOperand, self.__io_controller.asm_INP),            number_of_operands=1), # fmt: skip
            0x17: MetaInstruction(mnemonic="OUT",  method=cast(Instruction_OneOperand, self.__io_controller.asm_OUT),            number_of_operands=1), # fmt: skip
            0x18: MetaInstruction(mnemonic="OUTC", method=cast(Instruction_OneOperand, self.__io_controller.asm_OUTC),           number_of_operands=1), # fmt: skip
            # Interrupt operations
            0xFF: MetaInstruction(mnemonic="IRET", method=cast(Instruction_ZeroOperands, self.__interrupt_controller.asm_IRET),  number_of_operands=0), # fmt: skip
        }
        self.__operand_type_set: OperandTypeSet = {
            0x00: OperandType(name="register", operand_size_byte=1),
            0x01: OperandType(name="value",    operand_size_byte=2),
        }
        self.__control_unit: ControlUnit = ControlUnit(self.__memory, self.__instruction_set, self.__register_set, self.__operand_type_set) # fmt: skip

    def __run_interrupt_sub_routine(self, address: Byte) -> None:
        self.__interrupt_controller.save_current_context()
        self.__run_CPU(address)

    def __handle_interrupt(self) -> None:
        interrupt: Interrupt = self.__interrupt_controller.get_next_interrupt() # fmt: skip
        interrupt_command: Byte = interrupt.interrupt_command
        interrupt_address: Byte = interrupt.memory_address
        interrupt_args: bytearray = interrupt.arguments
        if interrupt_command == 0x00:
            self.load_program(interrupt_address, interrupt_args)
        elif interrupt_command == 0x01:
            self.__run_interrupt_sub_routine(interrupt_address)
        else:
            print(f"Unknwown command: {interrupt_command}")
            return

    def __run_CPU(self, address: Byte) -> None:
        self.__control_unit.set_program_counter(address)
        self.__register_set[0x06].set(address)
        try:
            while True:
                if self.__interrupt_controller.has_interrupt:
                    self.__handle_interrupt()
                self.__control_unit.clock()
        except StopIteration as e:
            print(f"StopIteration: {e}")
            self.__run_CPU(0x00)  # jump to initial CPU loop
        except StopAsyncIteration:
            print("IRET")
            return

    def start(self, address: Byte = 0x00) -> None:
        self.__interrupt_controller.start_interrupt_listener()
        self.__run_CPU(address)

    def load_program(self, address: Byte, program: bytearray) -> None:
        self.__memory.set_with_address(address, program)
