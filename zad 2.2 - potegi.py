class Potegowanie:
    def __init__(self, a, n):
        self.a = a
        self.n = n
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.n:
            value = self.a ** self.index
            self.index += 1
            return value
        else:
            raise StopIteration

generator = Potegowanie(3, 5)
for power in generator:
    print(power)