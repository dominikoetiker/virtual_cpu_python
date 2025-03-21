from base.Register import Register
import socket
import threading
from typing import Dict, List, Tuple


class InterruptController:
    def __init__(self, register_set: Dict[int, Tuple[str, Register]]):
        self.has_interrupt: bool = False
        self.__interrupt_vector_table: List[Tuple[int, int, List[int]]] = []
        self.__register_set: Dict[int, Tuple[str, Register]] = register_set
        self.__interrupt_context_memory: List[
            Tuple[int, int, int, int, int, int, int]
        ] = []
        self.__start_interrupt_listener()

    def get_next_interrupt(self) -> Tuple[int, int, List[int]]:
        interrupt: Tuple[int, int, List[int]] = self.__interrupt_vector_table.pop(0)
        print(f"DEBUG: interrupt: {interrupt}")
        if len(self.__interrupt_vector_table) == 0:
            print(
                f"DEBUG: len of __interrupt_vector_table is == 0: {self.__interrupt_vector_table}"
            )
            self.has_interrupt = False
        return interrupt

    def save_current_context(self):
        context: Tuple[int, int, int, int, int, int, int] = (
            self.__register_set[0x00][1].get(),
            self.__register_set[0x01][1].get(),
            self.__register_set[0x02][1].get(),
            self.__register_set[0x03][1].get(),
            self.__register_set[0x04][1].get(),
            self.__register_set[0x05][1].get(),
            self.__register_set[0x06][1].get(),
        )
        self.__interrupt_context_memory.append(context)
        print(f"DEBUG: context stored: {context}")
        print(
            f"DEBUG: self.__interrupt_context_memory: {self.__interrupt_context_memory}"
        )

    def asm_IRET(self):
        self.recreate_last_context()
        raise StopAsyncIteration("IRET called")

    def recreate_last_context(self):
        last_context: Tuple[int, int, int, int, int, int, int] = (
            self.__interrupt_context_memory.pop()
        )
        self.__register_set[0x00][1].set(last_context[0])
        self.__register_set[0x01][1].set(last_context[1])
        self.__register_set[0x02][1].set(last_context[2])
        self.__register_set[0x03][1].set(last_context[3])
        self.__register_set[0x04][1].set(last_context[4])
        self.__register_set[0x05][1].set(last_context[5])
        self.__register_set[0x06][1].set(last_context[6])

    def __start_interrupt_listener(self):
        def interrupt_listener_thread():
            server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("localhost", 9999))
            server.listen(5)
            print(
                """
            CPU running
            Interrupt controller listening on port 9999
            Waiting for instructions
            LOAD TO_ADDRESS [bytes] = 0x00 0x... 0x... ...
                (Address has to be at least 0x0A)
            RUN ADDRESS = 0x01 0x..

            """
            )

            while True:
                client_socket: socket.socket = server.accept()[0]
                data: str = client_socket.recv(1024).decode("utf-8")
                self.__process_interrupt(data)
                client_socket.close()

        t: threading.Thread = threading.Thread(target=interrupt_listener_thread)
        t.daemon = True
        t.start()

    def __process_interrupt(self, interrupt_message: str):
        interrupt_message_parts: List[str] = interrupt_message.split(" ")
        try:
            interrupt_command: int = int(interrupt_message_parts[0], 0)
        except ValueError as e:
            print(f"Error in interrupt command, try again: {e}")
            return
        try:
            address: int = int(interrupt_message_parts[1], 0)
        except ValueError as e:
            print(f"Error in address, try again: {e}")
            return
        if (interrupt_command == 0x00) and (address < 0x0A):
            print("Error in address, LOAD address has to by at least 0x0A")
        try:
            arguments: List[int] = [int(x, 0) for x in interrupt_message_parts[2:]]
        except ValueError as e:
            print(f"Error ein program, try again: {e}")
            return
        pending_interrupt: Tuple[int, int, List[int]] = (
            interrupt_command,
            address,
            arguments,
        )
        self.__interrupt_vector_table.append(pending_interrupt)
        self.has_interrupt = True
