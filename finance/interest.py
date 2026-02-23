class Interest:
    def __init__(self, i):
        self.i = i
        self.v = 1 / (1 + i)

    def discount(self, t):
        return self.v ** t