from cpu import Cpu

def main():
    my_cpu: Cpu = Cpu()
    my_cpu.asm_NOP()

    my_cpu.asm_MOV(my_cpu.R0, 0xaabb)
    my_cpu.asm_MOV(my_cpu.R1, 0x0001)
    my_cpu.asm_ADD(my_cpu.R0, my_cpu.R0, my_cpu.R1)
    my_cpu.asm_OUT(my_cpu.R0)
    

if __name__ == "__main__":
    main()