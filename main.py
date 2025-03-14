from CentralProcessingUnit import CentralProcessingUnit


def main():
    my_cpu: CentralProcessingUnit = CentralProcessingUnit()

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
            0x01,  # PC: 0x001a: HLT
        ]
    )

    example_program_2 = bytearray(
        [
            # Example: Adding two numbers and outputting the result
            0x02, 0x01, 0x00, 0x05, 0x00,  # MOV R0, 5 # fmt: skip
            0x02, 0x01, 0x01, 0x03, 0x00,  # MOV R1, 3 # fmt: skip
            0x08, 0x00, 0x00, 0x00, 0x01,  # ADD R0, R0, R1 # fmt: skip
            0x17, 0x00, 0x00,  # OUT R0 # fmt: skip
            0x01,  # HLT # fmt: skip
        ]
    )

    example_program_3 = bytearray(
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

            # HLT
            0x01, # PC: 0x001d: HLT
        ]
    )

    example_program_4 = bytearray(
        [
            # Example: Output all Fibonacci numbers up to user defined limit
            # set_limit:
                # INP R0
                0x16, # PC: 0x0000: INP
                0x00, # PC: 0x0001: last_operand_type (register)
                0x00, # PC: 0x0002: operand_1 (register 0)

                # STR R0, 0x80 (store the limit in memory)
                0x15, # PC: 0x0003: STR
                0x01, # PC: 0x0004: last_operand_type (value)
                0x00, # PC: 0x0005: operand_1 (register 0)
                0x80, # PC: 0x0006: second byte of address
                0x00, # PC: 0x0007: first byte of address

            # store_first_two_numbers:
                # MOV R0, 0
                0x02, # PC: 0x0008: MOV
                0x01, # PC: 0x0009: last_operand_type (value)
                0x00, # PC: 0x000a: operand_1 (register 0)
                0x00, # PC: 0x000b: second byte of value 0
                0x00, # PC: 0x000c: first byte of value 0

                # STR R0, 0x82 (store the first number in memory)
                0x15, # PC: 0x000d: STR
                0x01, # PC: 0x000e: last_operand_type (value)
                0x00, # PC: 0x000f: operand_1 (register 0)
                0x82, # PC: 0x0010: second byte of address
                0x00, # PC: 0x0011: first byte of address

                # BL 0x2c (is_current_number_greater_than_limit)
                0x06, # PC: 0x0012: BL
                0x01, # PC: 0x0013: last_operand_type (value)
                0x2c, # PC: 0x0014: second byte of address (is_current_number_greater_than_limit)
                0x00, # PC: 0x0015: first byte of address (is_current_number_greater_than_limit)

                # LDR R0, 0x82 (load the first number from memory)
                0x14, # PC: 0x0016: LDR
                0x01, # PC: 0x0017: last_operand_type (value)
                0x00, # PC: 0x0018: operand_1 (register 0)
                0x82, # PC: 0x0019: second byte of address
                0x00, # PC: 0x001a: first byte of address

                # OUT R0
                0x17, # PC: 0x001b: OUT
                0x00, # PC: 0x001c: last_operand_type (register)
                0x00, # PC: 0x001d: operand_1 (register 0)

                # MOV R0, 1
                0x02, # PC: 0x001e: MOV
                0x01, # PC: 0x001f: last_operand_type (value)
                0x00, # PC: 0x0020: operand_1 (register 0)
                0x01, # PC: 0x0021: second byte of value 1
                0x00, # PC: 0x0022: first byte of value 1

                # STR R0, 0x84 (store the second number in memory)
                0x15, # PC: 0x0023: STR
                0x01, # PC: 0x0024: last_operand_type (value)
                0x00, # PC: 0x0025: operand_1 (register 0)
                0x84, # PC: 0x0026: second byte of address
                0x00, # PC: 0x0027: first byte of address

                # B 0x47 (print_fibonacci_loop)
                0x05, # PC: 0x0028: B
                0x01, # PC: 0x0029: last_operand_type (value)
                0x47, # PC: 0x002a: second byte of address (print_fibonacci_loop)
                0x00, # PC: 0x002b: first byte of address (print_fibonacci_loop)


            # is_current_number_greater_than_limit:
                # LDR R1, 0x80 (load the limit from memory)
                0x14, # PC: 0x002c: LDR
                0x01, # PC: 0x002d: last_operand_type (value)
                0x01, # PC: 0x002e: operand_1 (register 1)
                0x80, # PC: 0x002f: second byte of address
                0x00, # PC: 0x0030: first byte of address

                # SUB R0, R0, R1 (R0 = R0 - R1) (current_number - limit)
                0x09, # PC: 0x0031: SUB
                0x00, # PC: 0x0032: last_operand_type (register)
                0x00, # PC: 0x0033: operand_1 (register 0)
                0x00, # PC: 0x0034: operand_2 (register 0)
                0x01, # PC: 0x0035: operand_3 (register 1)

                # AND R0, R0, 0b1000 0000 0000 0000 (R0 = R0 & 0b1000 0000 0000 0000) (extract the most significant bit)
                0x0D, # PC: 0x0036: AND
                0x01, # PC: 0x0037: last_operand_type (value)
                0x00, # PC: 0x0038: operand_1 (register 0)
                0x00, # PC: 0x0039: operand_2 (register 0)
                0x00, # PC: 0x003a: second byte of value 0b1000 0000 0000 0000
                0x80, # PC: 0x003b: first byte of value 0b1000 0000 0000 0000

                # CMP R0, 0 (compare the result with 0. If the most significant bit is 1 (sign), the current number is less than the limit)
                0x13, # PC: 0x003c: CMP
                0x01, # PC: 0x003d: last_operand_type (value)
                0x00, # PC: 0x003e: operand_1 (register 0)
                0x00, # PC: 0x003f: second byte of value 0
                0x00, # PC: 0x0040: first byte of value 0

                # BNE 0x46 (if the current number is not greater than the limit, jump to jmp_back)
                0x04, # PC: 0x0041: BNE
                0x01, # PC: 0x0042: last_operand_type (value)
                0x46, # PC: 0x0043: second byte of address (jmp_back)
                0x00, # PC: 0x0044: first byte of address (jmp_back)

                # HLT (if the current number is greater than the limit, halt the program)
                0x01, # PC: 0x0045: HLT

                # jmp_back:
                    # BX (jump back, where came from)
                    0x07, # PC: 0x0046: BX

            # print_fibonacci_loop:
                # LDR R0, 0x82 (load the first number from memory)
                0x14, # PC: 0x0047: LDR
                0x01, # PC: 0x0048: last_operand_type (value)
                0x00, # PC: 0x0049: operand_1 (register 0)
                0x82, # PC: 0x004a: second byte of address
                0x00, # PC: 0x004b: first byte of address

                # LDR R1, 0x84 (load the second number from memory)
                0x14, # PC: 0x004c: LDR
                0x01, # PC: 0x004d: last_operand_type (value)
                0x01, # PC: 0x004e: operand_1 (register 1)
                0x84, # PC: 0x004f: second byte of address
                0x00, # PC: 0x0050: first byte of address

                # STR R0, 0x84 (store the first number in memory)
                0x15, # PC: 0x0051: STR
                0x01, # PC: 0x0052: last_operand_type (value)
                0x00, # PC: 0x0053: operand_1 (register 0)
                0x84, # PC: 0x0054: second byte of address
                0x00, # PC: 0x0055: first byte of address

                # ADD R0, R0, R1 (R0 = R0 + R1) (current_number = first_number + second_number)
                0x08, # PC: 0x0056: ADD
                0x00, # PC: 0x0057: last_operand_type (register)
                0x00, # PC: 0x0058: operand_1 (register 0)
                0x00, # PC: 0x0059: operand_2 (register 0)
                0x01, # PC: 0x005a: operand_3 (register 1)

                # STR R0, 0x82 (store the current number in memory)
                0x15, # PC: 0x005b: STR
                0x01, # PC: 0x005c: last_operand_type (value)
                0x00, # PC: 0x005d: operand_1 (register 0)
                0x82, # PC: 0x005e: second byte of address
                0x00, # PC: 0x005f: first byte of address

                # BL 0x2c (is_current_number_greater_than_limit)
                0x06, # PC: 0x0060: BL
                0x01, # PC: 0x0061: last_operand_type (value)
                0x2c, # PC: 0x0062: second byte of address (is_current_number_greater_than_limit)
                0x00, # PC: 0x0063: first byte of address (is_current_number_greater_than_limit)

                # LDR R0, 0x82 (load the current number from memory)
                0x14, # PC: 0x0064: LDR
                0x01, # PC: 0x0065: last_operand_type (value)
                0x00, # PC: 0x0066: operand_1 (register 0)
                0x82, # PC: 0x0067: second byte of address
                0x00, # PC: 0x0068: first byte of address

                # OUT R0
                0x17, # PC: 0x0069: OUT
                0x00, # PC: 0x006a: last_operand_type (register)
                0x00, # PC: 0x006b: operand_1 (register 0)

                # B 0x47 (print_fibonacci_loop)
                0x05, # PC: 0x006c: B
                0x01, # PC: 0x006d: last_operand_type (value)
                0x47, # PC: 0x006e: second byte of address (print_fibonacci_loop)
                0x00, # PC: 0x006f: first byte of address (print_fibonacci_loop)
        ]
    )

    my_cpu.load_program(example_program_4)
    my_cpu.run()


if __name__ == "__main__":
    main()
