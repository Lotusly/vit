class A:
    def __init__(self):
        self.i = 4

    def func_to_pass(self):
        print(self.i)

    def func_make_b(self):
        return B(self.func_to_pass)


class B:
    def __init__(self, func):
        self.func = func

    def func_to_call(self):
        self.func()

a = A()
b = a.func_make_b()
b.func_to_call()

