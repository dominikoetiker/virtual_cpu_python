import socket
import threading
from typing import List, Tuple


class InterruptController:
    def __init__(self):
        self.has_interrupt: bool = False
        self.__pending_interrupts: List[Tuple[int, int, List[int]]] = []
        self.__start_interrupt_listener()

    def get_next_interrupt(self) -> Tuple[int, int, List[int]]:
        interrupt: Tuple[int, int, List[int]] = self.__pending_interrupts.pop(0)
        if len(self.__pending_interrupts) == 0:
            self.has_interrupt = False
        return interrupt

    def __start_interrupt_listener(self):
        def interrupt_listener_thread():
            server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(("localhost", 9999))
            server.listen(5)
            print(
                """
            CPU running
            Interrupt controller listening on localhost port 9999
            Waiting for instructions
            LOAD TO_ADDRESS [bytes] = 0x00 0x... 0x... ...
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
        print(self.__pending_interrupts)
        try:
            address: int = int(interrupt_message_parts[1], 0)
        except ValueError as e:
            print(f"Error in address, try again: {e}")
            return
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
        self.__pending_interrupts.append(pending_interrupt)
        self.has_interrupt = True
        print(self.__pending_interrupts)
