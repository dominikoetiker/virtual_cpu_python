import socket
import threading
from data_types import Byte, CPUContext, Interrupt, RegisterSet


class InterruptController:
    def __init__(self, register_set: RegisterSet):
        self.has_interrupt: bool = False
        self.__interrupt_vector_table: list[Interrupt] = []
        self.__register_set: RegisterSet = register_set
        self.__interrupt_context_memory: list[CPUContext] = []

    def __recreate_last_context(self) -> None:
        last_context: CPUContext = self.__interrupt_context_memory.pop()
        self.__register_set[0x00].set(last_context.R0)
        self.__register_set[0x01].set(last_context.R1)
        self.__register_set[0x02].set(last_context.R2)
        self.__register_set[0x03].set(last_context.R3)
        self.__register_set[0x04].set(last_context.R4)
        self.__register_set[0x05].set(last_context.R5)
        self.__register_set[0x06].set(last_context.R6)

    def __interrupt_listener_thread(self) -> None:
        server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 9999))
        server.listen(5)
        print(
            """
CPU running
Waiting for instructions

"""
        )

        while True:
            client_socket: socket.socket = server.accept()[0]
            data: str = client_socket.recv(1024).decode("utf-8")
            self.__process_interrupt(data)
            client_socket.close()

    def __process_interrupt(self, interrupt_message: str) -> None:
        interrupt_message_lines: list[str] = interrupt_message.split("\n")
        interrupt_message_bytes: list[str] = []
        for line in interrupt_message_lines:
            line_parts: list[str] = line.split(" ")
            for byte in line_parts:
                if byte != "":
                    interrupt_message_bytes.append(byte)
        try:
            interrupt_command: Byte = int(interrupt_message_bytes[0], 0)
        except ValueError as e:
            print(f"Error in interrupt command, try again: {e}")
            return
        try:
            address: Byte = int(interrupt_message_bytes[1], 0)
        except ValueError as e:
            print(f"Error in address, try again: {e}")
            return
        if (interrupt_command == 0x00) and (address < 0x0A):
            print("Error in address, LOAD address has to by at least 0x0A")
        try:
            arguments: bytearray = bytearray(
                [int(x, 0) for x in interrupt_message_bytes[2:]]
            )
        except ValueError as e:
            print(f"Error ein program, try again: {e}")
            return
        pending_interrupt: Interrupt = Interrupt(
            interrupt_command=interrupt_command,
            memory_address=address,
            arguments=arguments,
        )
        self.__interrupt_vector_table.append(pending_interrupt)
        self.has_interrupt = True

    def start_interrupt_listener(self) -> None:
        t: threading.Thread = threading.Thread(target=self.__interrupt_listener_thread)
        t.daemon = True
        t.start()

    def get_next_interrupt(self) -> Interrupt:
        interrupt: Interrupt = self.__interrupt_vector_table.pop(0)
        if len(self.__interrupt_vector_table) == 0:
            self.has_interrupt = False
        return interrupt

    def save_current_context(self) -> None:
        context: CPUContext = CPUContext(
            R0=self.__register_set[0x00].get(),
            R1=self.__register_set[0x01].get(),
            R2=self.__register_set[0x02].get(),
            R3=self.__register_set[0x03].get(),
            R4=self.__register_set[0x04].get(),
            R5=self.__register_set[0x05].get(),
            R6=self.__register_set[0x06].get(),
        )
        self.__interrupt_context_memory.append(context)

    def asm_IRET(self) -> None:
        self.__recreate_last_context()
        raise StopAsyncIteration("IRET called")
