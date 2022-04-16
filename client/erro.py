class TimerError(Exception):

    def __init__(self, timeout, message="Erro de timeout"):
        self.timeout = timeout
        self.message = message
        super().__init__(self.timeout,self.message)