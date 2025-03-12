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
            # check if a is > than b
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

    my_cpu.load_program(example_program_3)
    my_cpu.run()


if __name__ == "__main__":
    main()
