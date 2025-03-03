from cpu import Cpu


def main():
    my_cpu: Cpu = Cpu()
    my_cpu.asm_NOP()

    my_cpu.asm_INP(my_cpu.R0)
    my_cpu.asm_OUT(my_cpu.R0)

    my_cpu.asm_MUL(my_cpu.R1, my_cpu.R0, 2)
    my_cpu.asm_OUT(my_cpu.R1)

    my_cpu.asm_DIV(my_cpu.R1, my_cpu.R0, 2)
    my_cpu.asm_OUT(my_cpu.R1)

    my_cpu.asm_ADD(my_cpu.R1, my_cpu.R0, 2)
    my_cpu.asm_OUT(my_cpu.R1)

    my_cpu.asm_SUB(my_cpu.R1, my_cpu.R0, 2)
    my_cpu.asm_OUT(my_cpu.R1)

    my_cpu.asm_MOV(my_cpu.R0, 0x1)
    my_cpu.asm_MOV(my_cpu.R1, 0x2)

    my_cpu.asm_CMP(my_cpu.R0, my_cpu.R1)
    print(my_cpu.Z)

    my_cpu.asm_MOV(my_cpu.R0, 0xA)
    my_cpu.asm_MOV(my_cpu.R1, 0xA)

    my_cpu.asm_CMP(my_cpu.R0, my_cpu.R1)
    print(my_cpu.Z)

    my_cpu.asm_HLT()


if __name__ == "__main__":
    main()
