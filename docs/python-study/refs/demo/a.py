class A:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        if isinstance(other, A):
            print('比较 A 与 A')
            return other.value == self.value
        if isinstance(other, B):
            print('Comparing an A with a B')
            return other.value == self.value
        print('Could not compare A with the other class')
        return NotImplemented


class B:
    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        if isinstance(other, B):
            print('Comparing a B with another B')
            return other.value == self.value
        print('Could not compare B with the other class')
        return NotImplemented