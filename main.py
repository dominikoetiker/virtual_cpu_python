from CentralProcessingUnit import CentralProcessingUnit


def main() -> None:
    cpu: CentralProcessingUnit = CentralProcessingUnit()
    system_loop = bytearray(
        [
            # System loop
            0x05,  # PC: 0x0000: B
            0x01,  # PC: 0x0001: last_operand_type (value)
            0x00,  # PC: 0x0002: second byte of address (system_loop)
            0x00,  # PC: 0x0003: first byte of address (system_loop)
        ]
    )
    cpu.load_program(0x00, system_loop)
    cpu.start()


if __name__ == "__main__":
    main()
