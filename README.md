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
- **Program Base Address Register**: R6 (holds the base address of the current program)

### Flags

- **Z**: Zero flag - Set when a result is zero, used for conditional operations

### Memory System

- RAM with configurable size (default: 1024 bytes)
- Support for address-based memory access

### Interrupt System

The CPU now features a complete interrupt handling system:

- **Interrupt Controller**: Manages interrupt requests and context switching
- **Socket-based Interface**: Allows external programs to trigger interrupts while the CPU is running
- **Context Preservation**: Automatically saves and restores CPU state during interrupts
- **Support for Multiple Programs**: Load and execute multiple programs without rebooting the CPU

#### Interrupt Operations

| Command | Description                                       |
| ------- | ------------------------------------------------- |
| 0x00    | Load a program into memory at a specified address |
| 0x01    | Execute a program at a specified address          |

## Bytecode Format

### Instruction Set

| Opcode                    | Mnemonic | Assembly instruction Format | Description                                              | Flags Affected |
| ------------------------- | -------- | --------------------------- | -------------------------------------------------------- | -------------- |
| **Control Operations**    |
| 0x00                      | NOP      | `NOP`                       | No operation, processor continues to next instruction    | None           |
| 0x01                      | HLT      | `HLT`                       | Halt execution, go to idle state                         | None           |
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
| 0x18                      | OUTC     | `OUTC Rd`                   | Output character from Rd to console                      | None           |
| **Interrupt Operations**  |
| 0xFF                      | IRET     | `IRET`                      | Return from interrupt, restoring previous CPU state      | None           |

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

| Code | Register | Description                   |
| ---- | -------- | ----------------------------- |
| 0x00 | R0       | General Purpose Register 0    |
| 0x01 | R1       | General Purpose Register 1    |
| 0x02 | R2       | Output Register               |
| 0x03 | R3       | Link Register                 |
| 0x04 | R4       | Memory Byte Register          |
| 0x05 | R5       | Program Counter               |
| 0x06 | R6       | Program Base Address Register |

### Instruction Format

Each instruction is represented as a sequence of bytes in the following format:

```
Opcode [LastOperandType, Oberand1 [Operand2 [Operand3 ...]]]
```

Where:

- **Opcode**: 1 byte
- **Last Operand Type**: 1 byte
- **Operands**: 0-n bytes (depending on the instruction), using little-endian byte order

**Relative Addressing**:
The CPU supports relative addressing for branch instructions. The address is calculated as an offset from the current Program Base Address Register (R6).

## Usage

Best way to run and interact with the CPU is with two terminal windows. In one terminal, run the CPU simulator, and in the other, use the provided scripts to load and execute programs. You can for example use tmux to split the terminal window or open two separate terminal windows.

### Running the CPU

To run the CPU simulator, execute the following command:

```bash
python main.py
```

### Dynamic Program Loading

Programs can now be loaded and executed while the CPU is running using the provided scripts:

```bash
# Load a program into memory
./program_loader.sh <program_file.mem> <memory_address>

# Execute a program at a specified address
./program_starter.sh <memory_address>
```

**Note**: The memory address for programs should be equal or greater than 0x0A (10 in decimal). The Addresses 0x00 to 0x09 are reserved for the CPU's idle state.

For example:

```bash
# Load Hello World program at address 0x0A
./program_loader.sh hello_world.mem 0x0A

# Run the Hello World program
./program_starter.sh 0x0A

# Load Fibonacci sequence generator at address 0xA1
./program_loader.sh fibonacci.mem 0xA1

# Run the Fibonacci sequence generator
./program_starter.sh 0xA1
```

**Note**: Make the scripts executable before running them:

```bash
chmod +x program_loader.sh program_starter.sh
```

## Example Programs

Here are some example programs written as commented bytearrays that can be loaded and executed by the CPU.

**Note**: To load these programs dynamically, you need to put the hex values without commas and without the comments, just separated by spaces and/or new lines (like this: `0x02 0x01 0x00 0x48 0x00 0x18 0x00 0x00 ...`), in a file with the `.mem` extension (using the extension is optional, but it helps to identify the file type).

<details>
<summary>Hello World</summary>

This program outputs "Hello World" to the console.

```python
hello_world = bytearray([
    # Hello World program
    0x02, 0x01, 0x00, 0x48, 0x00,  # MOV R0, 72 (H)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x65, 0x00,  # MOV R0, 101 (e)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x6c, 0x00,  # MOV R0, 108 (l)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x6c, 0x00,  # MOV R0, 108 (l)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x6f, 0x00,  # MOV R0, 111 (o)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x20, 0x00,  # MOV R0, 32 (space)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x57, 0x00,  # MOV R0, 87 (W)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x6f, 0x00,  # MOV R0, 111 (o)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x72, 0x00,  # MOV R0, 114 (r)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x6c, 0x00,  # MOV R0, 108 (l)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x64, 0x00,  # MOV R0, 100 (d)
    0x18, 0x00, 0x00,              # OUTC R0
    0x02, 0x01, 0x00, 0x0a, 0x00,  # MOV R0, 10 (LF)
    0x18, 0x00, 0x00,              # OUTC R0
    0xFF,                          # IRET
])
```

</details>
<details>
<summary>Add two numbers</summary>

This program adds two numbers and outputs the result.

```python
 add_two_numbers = bytearray(
     [
         # Example: Adding two numbers and outputting the result
         0x02, 0x01, 0x00, 0x05, 0x00,  # MOV R0, 5 # fmt: skip
         0x02, 0x01, 0x01, 0x03, 0x00,  # MOV R1, 3 # fmt: skip
         0x08, 0x00, 0x00, 0x00, 0x01,  # ADD R0, R0, R1 # fmt: skip
         0x17, 0x00, 0x00,  # OUT R0 # fmt: skip
         0xFF,  # IRET # fmt: skip
     ]
 )

```

</details>
<details>
<summary>Adding numbers with user input</summary>

This program adds two numbers, gets a new number from the user, adds it to the sum, and outputs the result.

```python
example_program_1 = bytearray(
    [
        # Example: Adding two numbers, getting a new number from the user, adding it to the sum and outputting the result
        0x02,  # PC: 0x0000: MOV
        0x01,  # PC: 0x0001: last_operand_type (value)
        0x00,  # PC: 0x0002: operand_1 (register 0)
        0x01,  # PC: 0x0003: second byte of value 1
        0x00,  # PC: 0x0004: first byte of value 1
        0x02,  # PC: 0x0005: MOV
        0x01,  # PC: 0x0006: last_operand_type (value)
        0x01,  # PC: 0x0007: operand_1 (register 1)
        0x02,  # PC: 0x0008: second byte of value 2
        0x00,  # PC: 0x0009: first byte of value 2
        0x08,  # PC: 0x000a: ADD
        0x00,  # PC: 0x000b: last_operand_type (register)
        0x00,  # PC: 0x000c: operand_1 (result register: register 0)
        0x00,  # PC: 0x000d: operand_2 (summand 1: register 0)
        0x01,  # PC: 0x000e: operand_3 (summand 2: register 1)
        0x16,  # PC: 0x000f: INP
        0x00,  # PC: 0x0010: last_operand_type (register)
        0x01,  # PC: 0x0011: operand_1 (register 1)
        0x08,  # PC: 0x0012: ADD
        0x00,  # PC: 0x0013: last_operand_type (register)
        0x00,  # PC: 0x0014: operand_1 (result register: register 0)
        0x00,  # PC: 0x0015: operand_2 (summand 1: register 0)
        0x01,  # PC: 0x0016: operand_3 (summand 2: register 1)
        0x17,  # PC: 0x0017: OUT
        0x00,  # PC: 0x0018: last_operand_type (register)
        0x00,  # PC: 0x0019: operand_1 (register 0)
        0xFF,  # PC: 0x001a: IRET
    ]
)
```

</details>
<details>
<summary>Check if one number is greater than the other</summary>

This program checks if a number is greater than another and outputs the result.

```python
is_greater_than: bytearray = bytearray(
    [
        # Example: check if a is > than b
        # INP R0 (a)
        0x16, # PC: 0x0000: INP
        0x00, # PC: 0x0001: last_operand_type (register)
        0x00, # PC: 0x0002: operand_1 (register 0)

        # INP R1 (b)
        0x16, # PC: 0x0003: INP
        0x00, # PC: 0x0004: last_operand_type (register)
        0x01, # PC: 0x0005: operand_1 (register 1)

        # SUB R0, R0, R1 (R0 = R0 - R1) (a - b)
        0x09, # PC: 0x0006: SUB
        0x00, # PC: 0x0007: last_operand_type (register)
        0x00, # PC: 0x0008: operand_1 (register 0)
        0x00, # PC: 0x0009: operand_2 (register 0)
        0x01, # PC: 0x000a: operand_3 (register 1)

        # AND R0, R0, 0b1000 0000 0000 0000 (R0 = R0 & 0b1000 0000 0000 0000) (check if the most significant bit of R0 is set to 1)
        0x0D, # PC: 0x000b: AND
        0x01, # PC: 0x000c: last_operand_type (value)
        0x00, # PC: 0x000d: operand_1 (register 0)
        0x00, # PC: 0x000e: operand_2 (register 0)
        0x00, # PC: 0x000f: second byte of value 0b1000 0000 0000 0000
        0x80, # PC: 0x0010: first byte of value 0b1000 0000 0000 0000

        # LSR R0, R0, 15 (R0 = R0 >> 15) (shift the most significant bit to the least significant bit)
        0x12, # PC: 0x0011: LSR
        0x01, # PC: 0x0012: last_operand_type (value)
        0x00, # PC: 0x0013: operand_1 (register 0)
        0x00, # PC: 0x0014: operand_2 (register 0)
        0x0f, # PC: 0x0015: second byte of value 15
        0x00, # PC: 0x0016: first byte of value 15

        # OUT R0 (if output is 1, a < b, if output is 0, a >= b)
        0x17, # PC: 0x0017: OUT
        0x00, # PC: 0x0018: last_operand_type (register)
        0x00, # PC: 0x0019: operand_1 (register 0)

        # IRET
        0xFF, # PC: 0x001d: IRET
    ]
)
```

</details>
<details>
<summary>Fibonacci sequence generator</summary>

This program calculates and outputs the Fibonacci sequence up to a specified maximum value.

```python
fibonacci: bytearray = bytearray(
    [
        # Example: Output all Fibonacci numbers up to user defined limit
        # set_limit:
        # INP R0
        0x16,  # PC: 0x0000: INP
        0x00,  # PC: 0x0001: last_operand_type (register)
        0x00,  # PC: 0x0002: operand_1 (register 0)
        # STR R0, 0x80 (store the limit in memory)
        0x15,  # PC: 0x0003: STR
        0x01,  # PC: 0x0004: last_operand_type (value)
        0x00,  # PC: 0x0005: operand_1 (register 0)
        0x80,  # PC: 0x0006: second byte of address
        0x00,  # PC: 0x0007: first byte of address
        # store_first_two_numbers:
        # MOV R0, 0
        0x02,  # PC: 0x0008: MOV
        0x01,  # PC: 0x0009: last_operand_type (value)
        0x00,  # PC: 0x000a: operand_1 (register 0)
        0x00,  # PC: 0x000b: second byte of value 0
        0x00,  # PC: 0x000c: first byte of value 0
        # STR R0, 0x82 (store the first number in memory)
        0x15,  # PC: 0x000d: STR
        0x01,  # PC: 0x000e: last_operand_type (value)
        0x00,  # PC: 0x000f: operand_1 (register 0)
        0x82,  # PC: 0x0010: second byte of address
        0x00,  # PC: 0x0011: first byte of address
        # BL 0x2c (is_current_number_greater_than_limit)
        0x06,  # PC: 0x0012: BL
        0x01,  # PC: 0x0013: last_operand_type (value)
        0x2C,  # PC: 0x0014: second byte of address (is_current_number_greater_than_limit)
        0x00,  # PC: 0x0015: first byte of address (is_current_number_greater_than_limit)
        # LDR R0, 0x82 (load the first number from memory)
        0x14,  # PC: 0x0016: LDR
        0x01,  # PC: 0x0017: last_operand_type (value)
        0x00,  # PC: 0x0018: operand_1 (register 0)
        0x82,  # PC: 0x0019: second byte of address
        0x00,  # PC: 0x001a: first byte of address
        # OUT R0
        0x17,  # PC: 0x001b: OUT
        0x00,  # PC: 0x001c: last_operand_type (register)
        0x00,  # PC: 0x001d: operand_1 (register 0)
        # MOV R0, 1
        0x02,  # PC: 0x001e: MOV
        0x01,  # PC: 0x001f: last_operand_type (value)
        0x00,  # PC: 0x0020: operand_1 (register 0)
        0x01,  # PC: 0x0021: second byte of value 1
        0x00,  # PC: 0x0022: first byte of value 1
        # STR R0, 0x84 (store the second number in memory)
        0x15,  # PC: 0x0023: STR
        0x01,  # PC: 0x0024: last_operand_type (value)
        0x00,  # PC: 0x0025: operand_1 (register 0)
        0x84,  # PC: 0x0026: second byte of address
        0x00,  # PC: 0x0027: first byte of address
        # B 0x47 (print_fibonacci_loop)
        0x05,  # PC: 0x0028: B
        0x01,  # PC: 0x0029: last_operand_type (value)
        0x47,  # PC: 0x002a: second byte of address (print_fibonacci_loop)
        0x00,  # PC: 0x002b: first byte of address (print_fibonacci_loop)
        # is_current_number_greater_than_limit:
        # LDR R1, 0x80 (load the limit from memory)
        0x14,  # PC: 0x002c: LDR
        0x01,  # PC: 0x002d: last_operand_type (value)
        0x01,  # PC: 0x002e: operand_1 (register 1)
        0x80,  # PC: 0x002f: second byte of address
        0x00,  # PC: 0x0030: first byte of address
        # SUB R0, R0, R1 (R0 = R0 - R1) (current_number - limit)
        0x09,  # PC: 0x0031: SUB
        0x00,  # PC: 0x0032: last_operand_type (register)
        0x00,  # PC: 0x0033: operand_1 (register 0)
        0x00,  # PC: 0x0034: operand_2 (register 0)
        0x01,  # PC: 0x0035: operand_3 (register 1)
        # AND R0, R0, 0b1000 0000 0000 0000 (R0 = R0 & 0b1000 0000 0000 0000) (extract the most significant bit)
        0x0D,  # PC: 0x0036: AND
        0x01,  # PC: 0x0037: last_operand_type (value)
        0x00,  # PC: 0x0038: operand_1 (register 0)
        0x00,  # PC: 0x0039: operand_2 (register 0)
        0x00,  # PC: 0x003a: second byte of value 0b1000 0000 0000 0000
        0x80,  # PC: 0x003b: first byte of value 0b1000 0000 0000 0000
        # CMP R0, 0 (compare the result with 0. If the most significant bit is 1 (sign), the current number is less than the limit)
        0x13,  # PC: 0x003c: CMP
        0x01,  # PC: 0x003d: last_operand_type (value)
        0x00,  # PC: 0x003e: operand_1 (register 0)
        0x00,  # PC: 0x003f: second byte of value 0
        0x00,  # PC: 0x0040: first byte of value 0
        # BNE 0x46 (if the current number is not greater than the limit, jump to jmp_back)
        0x04,  # PC: 0x0041: BNE
        0x01,  # PC: 0x0042: last_operand_type (value)
        0x46,  # PC: 0x0043: second byte of address (jmp_back)
        0x00,  # PC: 0x0044: first byte of address (jmp_back)
        # IRET (if the current number is greater than the limit, halt the program)
        0xFF,  # PC: 0x0045: IRET
        # jmp_back:
        # BX (jump back, where came from)
        0x07,  # PC: 0x0046: BX
        # print_fibonacci_loop:
        # LDR R0, 0x82 (load the first number from memory)
        0x14,  # PC: 0x0047: LDR
        0x01,  # PC: 0x0048: last_operand_type (value)
        0x00,  # PC: 0x0049: operand_1 (register 0)
        0x82,  # PC: 0x004a: second byte of address
        0x00,  # PC: 0x004b: first byte of address
        # LDR R1, 0x84 (load the second number from memory)
        0x14,  # PC: 0x004c: LDR
        0x01,  # PC: 0x004d: last_operand_type (value)
        0x01,  # PC: 0x004e: operand_1 (register 1)
        0x84,  # PC: 0x004f: second byte of address
        0x00,  # PC: 0x0050: first byte of address
        # STR R0, 0x84 (store the first number in memory)
        0x15,  # PC: 0x0051: STR
        0x01,  # PC: 0x0052: last_operand_type (value)
        0x00,  # PC: 0x0053: operand_1 (register 0)
        0x84,  # PC: 0x0054: second byte of address
        0x00,  # PC: 0x0055: first byte of address
        # ADD R0, R0, R1 (R0 = R0 + R1) (current_number = first_number + second_number)
        0x08,  # PC: 0x0056: ADD
        0x00,  # PC: 0x0057: last_operand_type (register)
        0x00,  # PC: 0x0058: operand_1 (register 0)
        0x00,  # PC: 0x0059: operand_2 (register 0)
        0x01,  # PC: 0x005a: operand_3 (register 1)
        # STR R0, 0x82 (store the current number in memory)
        0x15,  # PC: 0x005b: STR
        0x01,  # PC: 0x005c: last_operand_type (value)
        0x00,  # PC: 0x005d: operand_1 (register 0)
        0x82,  # PC: 0x005e: second byte of address
        0x00,  # PC: 0x005f: first byte of address
        # BL 0x2c (is_current_number_greater_than_limit)
        0x06,  # PC: 0x0060: BL
        0x01,  # PC: 0x0061: last_operand_type (value)
        0x2C,  # PC: 0x0062: second byte of address (is_current_number_greater_than_limit)
        0x00,  # PC: 0x0063: first byte of address (is_current_number_greater_than_limit)
        # LDR R0, 0x82 (load the current number from memory)
        0x14,  # PC: 0x0064: LDR
        0x01,  # PC: 0x0065: last_operand_type (value)
        0x00,  # PC: 0x0066: operand_1 (register 0)
        0x82,  # PC: 0x0067: second byte of address
        0x00,  # PC: 0x0068: first byte of address
        # OUT R0
        0x17,  # PC: 0x0069: OUT
        0x00,  # PC: 0x006a: last_operand_type (register)
        0x00,  # PC: 0x006b: operand_1 (register 0)
        # B 0x47 (print_fibonacci_loop)
        0x05,  # PC: 0x006c: B
        0x01,  # PC: 0x006d: last_operand_type (value)
        0x47,  # PC: 0x006e: second byte of address (print_fibonacci_loop)
        0x00,  # PC: 0x006f: first byte of address (print_fibonacci_loop)
    ]
)
```

</details>

## Future Development

1. ✅ **Loader**: Implemented loader to load programs from files
2. ✅ **Interrupt Handling**: Implemented a complete interrupt system
3. **Assembler**: Create a tool to translate assembly language into bytecode

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
