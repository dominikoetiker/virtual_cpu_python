from cpu import Cpu

def main():
    my_cpu: Cpu = Cpu()
    my_cpu.asm_NOP()

    address: int = 0x3ff
    data: int = 0xff
    my_cpu.asm_STR(address, data)
    data: int = my_cpu.asm_LDR(address)

    print(f"Data at address {address}: {data}")
    print(my_cpu.memory.memory)
    

if __name__ == "__main__":
    main()