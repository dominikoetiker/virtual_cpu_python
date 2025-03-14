# Virtual CPU Python

A Python-based CPU simulator to understand the basic components and operations of a central processing unit.

## Project Overview

This project implements a virtual CPU in Python to simulate the basic operations and components of a computer's central processing unit.
The goal was to understand how CPUs work at a fundamental level by creating a working model with registers, memory, an arithmetic logic unit, a control unit, and I/O capabilities.

The CPU currently can execute programs provided as bytearrays.
The next planned feature is an assembler to translate human-readable assembly code into the bytecode format.

## Architecture

The virtual CPU implements a simplified architecture with the following components:

### Controllers

- **Arithmetic Logic Unit (ALU)**: Handles arithmetic and logical operations
- **Control Unit (CU)**: Manages the fetch-decode-execute cycle
- **Memory Controller**: Manages access to RAM
- **I/O Controller**: Handles input and output operations
- **Instruction Unit**: Manages program flow and control instructions

### Registers

- **General Purpose Registers**: R0, R1
- **Output Register**: R2
- **Link Register**: R3 (stores return addresses)
- **Memory Byte Register**: R4
- **Program Counter**: R5

### Flags

- **Z**: Zero flag - Set when a result is zero, used for conditional operations

### Memory System

- RAM with configurable size (default: 1024 bytes)
- Support for address-based memory access
- Memory tracking to manage used/free space (for now, it only marks memory as used and checks if it is used, but does not free it)

## Bytecode Format

### Instruction Set

| Opcode                    | Mnemonic | Assembly instruction Format | Description                                              | Flags Affected |
| ------------------------- | -------- | --------------------------- | -------------------------------------------------------- | -------------- |
| **Control Operations**    |
| 0x00                      | NOP      | `NOP`                       | No operation, processor continues to next instruction    | None           |
| 0x01                      | HLT      | `HLT`                       | Halt execution, stops the processor                      | None           |
| **Data Operations**       |
| 0x02                      | MOV      | `MOV Rd, Op2`               | Copy Op2 (register or value) into destination register   | None           |
| **Branch Operations**     |
| 0x03                      | BEQ      | `BEQ [addr]`                | Branch to address if Z flag is set (result was zero)     | None           |
| 0x04                      | BNE      | `BNE [addr]`                | Branch to address if Z flag is not set (result non-zero) | None           |
| 0x05                      | B        | `B [addr]`                  | Branch unconditionally to address                        | None           |
| 0x06                      | BL       | `BL [addr]`                 | Branch to address and store return address in R3         | None           |
| 0x07                      | BX       | `BX`                        | Branch to address stored in link register (R3)           | None           |
| **Arithmetic Operations** |
| 0x08                      | ADD      | `ADD Rd, Rn, Op2`           | Rd = Rn + Op2                                            | Z              |
| 0x09                      | SUB      | `SUB Rd, Rn, Op2`           | Rd = Rn - Op2                                            | Z              |
| 0x0A                      | MUL      | `MUL Rd, Rn, Op2`           | Rd = Rn \* Op2                                           | Z              |
| 0x0B                      | DIV      | `DIV Rd, Rn, Op2`           | Rd = Rn // Op2 (integer division)                        | Z              |
| 0x0C                      | MOD      | `MOD Rd, Rn, Op2`           | Rd = Rn % Op2 (modulo)                                   | Z              |
| **Logical Operations**    |
| 0x0D                      | AND      | `AND Rd, Rn, Op2`           | Rd = Rn & Op2 (bitwise AND)                              | Z              |
| 0x0E                      | ORR      | `ORR Rd, Rn, Op2`           | Rd = Rn \| Op2 (bitwise OR)                              | Z              |
| 0x0F                      | XOR      | `XOR Rd, Rn, Op2`           | Rd = Rn ^ Op2 (bitwise XOR)                              | Z              |
| 0x10                      | NOT      | `NOT Rd, Op2`               | Rd = ~Op2 (bitwise NOT)                                  | Z              |
| **Shift Operations**      |
| 0x11                      | LSL      | `LSL Rd, Rn, Op2`           | Rd = Rn << Op2 (logical shift left)                      | Z              |
| 0x12                      | LSR      | `LSR Rd, Rn, Op2`           | Rd = Rn >> Op2 (logical shift right)                     | Z              |
| **Compare Operations**    |
| 0x13                      | CMP      | `CMP Rn, Op2`               | Compare Rn with Op2 and set Z flag accordingly           | Z              |
| **Memory Operations**     |
| 0x14                      | LDR      | `LDR Rd, [addr]`            | Load value from memory address into Rd                   | None           |
| 0x15                      | STR      | `STR Rd, [addr]`            | Store value from Rd into memory address                  | None           |
| **I/O Operations**        |
| 0x16                      | INP      | `INP Rd`                    | Read input from user and store in Rd                     | None           |
| 0x17                      | OUT      | `OUT Rd`                    | Output value from Rd to console                          | None           |

Where:

- `Rd` = Destination register
- `Rn` = First operand register
- `Op2` = Second operand (register or immediate value)
- `[addr]` = Memory address (register or immediate value or label -> label is transformed by assembler to immediate value in Bytecode)
- `Z` = Zero flag (set when result is zero)

### Operand Types

| Code | Type     | Size (bytes) |
| ---- | -------- | ------------ |
| 0x00 | register | 1            |
| 0x01 | value    | 2            |

### Register Codes

| Code | Register |
| ---- | -------- |
| 0x00 | R0       |
| 0x01 | R1       |
| 0x02 | R2       |
| 0x03 | R3       |
| 0x04 | R4       |
| 0x05 | R5       |

### Instruction Format

Each instruction is represented as a sequence of bytes in the following format:

```
Opcode [LastOperandType, Oberand1 [Operand2 [Operand3 ...]]]
```

Where:

- **Opcode**: 1 byte
- **Last Operand Type**: 1 byte
- **Operands**: 0-n bytes (depending on the instruction), using little-endian byte order

## Usage

Currently, programs must be written as bytearrays. For example:

```python
# main.py
# ... other code

from CentralProcessingUnit import CentralProcessingUnit

# Create a new CPU instance
my_cpu = CentralProcessingUnit()

# Define a program as a bytearray
program = bytearray([
    # Example: Adding two numbers and outputting the result
    0x02, 0x01, 0x00, 0x05, 0x00,  # MOV R0, 5
    0x02, 0x01, 0x01, 0x03, 0x00,  # MOV R1, 3
    0x08, 0x00, 0x00, 0x00, 0x01,  # ADD R0, R0, R1
    0x17, 0x00, 0x00,              # OUT R0
    0x01                           # HLT
])

# Load and run the program
my_cpu.load_program(program)
my_cpu.run()

# ... other code
```

## Future Development

1. **Assembler**: Create a tool to translate assembly language into bytecode
2. **Loader**: Implement a loader to load programs from files
3. **Memory Management**: Improve the memory allocation and management system (e.g., free memory)

## Contributing

Contributions to this project are welcome! Whether you're a beginner or experienced developer, your input is valuable. Here are some ways to contribute:

- **Bug reports**: If you find an issue, please create a GitHub issue
- **Feature suggestions**: Have ideas for improvements? Let me know!
- **Code contributions**: Pull requests for new features or bug fixes are welcome
- **Documentation**: Help improve or extend the documentation
- **Educational feedback**: As this is a learning project, I appreciate feedback on the architecture and design

## License

This project is available under the MIT License. See the LICENSE file for details.

## Acknowledgments

This project was created as a personal learning exercise for me to understand CPU architecture.
It's meant to be educational rather than a production-ready CPU emulator.
