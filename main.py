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
            0x02, 0x01, 0x00, 0x05, 0x00,  # MOV R0, 5
            0x02, 0x01, 0x01, 0x03, 0x00,  # MOV R1, 3
            0x08, 0x00, 0x00, 0x00, 0x01,  # ADD R0, R0, R1
            0x17, 0x00, 0x00,  # OUT R0
            0x01,  # HLT
        ]
    )

    my_cpu.load_program(example_program_2)
    my_cpu.run()


if __name__ == "__main__":
    main()
