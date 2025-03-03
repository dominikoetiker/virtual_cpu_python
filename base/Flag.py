class Flag:
    def __init__(self, default_state: bool = False):
        self.isFlagSet: bool = default_state

    def set_is_zero(self, value: int):
        self.isFlagSet = value == 0
