class Pointer :
    def __init__(self, value) -> None:
        self.var = value
        self.killScript = False
    def get_var(self) :
        return self.var
    def set_var(self, newValue) :
        self.var = newValue
    def kill_script(self) :
        self.killScript = True
