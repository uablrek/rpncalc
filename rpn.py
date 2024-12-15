import math

class calc:
    def __init__(self):
        self.stack = []
        self.cmd = {
            "c": self.clear,
            "d": self.dup,
            "p": self.pop,
            "+": self.plus,
            "-": self.minus,
            "*": self.mul,
            "/": self.div,
            "pi": self.pi,
            "e": self.e,
            "sq": self.sq,
            "sqrt": self.sqrt,
            "pow": self.pow,
        }
    # Stack
    def top(self):
        return self.stack[-1]
    def clear(self):
        self.stack = []
    def push(self, n):
        self.stack.append(n)
    def pop(self):
        return self.stack.pop()
    def dup(self):
        n = self.stack.pop()
        self.stack.append(n)
        self.stack.append(n)
    # Basic arithmetic
    def plus(self):
        n = self.pop() + self.pop()
        self.stack.append(n)
        return n
    def minus(self):
        x = self.pop()
        n = self.pop() - x
        self.stack.append(n)
        return n
    def mul(self):
        n = self.pop() * self.pop()
        self.stack.append(n)
        return n
    def div(self):
        x = self.pop()
        n = self.pop() / x
        self.stack.append(n)
        return n
    # Constants
    def pi(self):
        self.stack.append(math.pi)
    def e(self):
        self.stack.append(math.e)
    # Math functions
    def sq(self):
        x = self.pop()
        n = x * x
        self.stack.append(n)
        return n
    def sqrt(self):
        n = math.sqrt(self.pop())
        self.stack.append(n)
        return n
    def pow(self):
        x = self.pop()
        n = math.pow(self.pop(), x)
        self.stack.append(n)
        return n
        
    # Execute a command token
    def exec(self, str):
        try:
            n = int(str, 0)
            self.stack.append(n)
            return
        except:
            try:
                n = float(str)
                self.stack.append(n)
                return
            except:
                pass
        return self.cmd[str]()
    # Eval a token sequence
    def eval(self, str):
        for t in str.split(' '):
            r = self.exec(t)
        return r
