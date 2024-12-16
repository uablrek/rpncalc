import math

class calc:
    def __init__(self):
        self.degrees = False
        self.stack = []
        self.cmd = {
            "p": self.pop,
            "c": self.clear,
            "d": self.dup,
            "w": self.swap,            
            "+": self.plus,
            "-": self.minus,
            "*": self.mul,
            "x": self.mul,
            "/": self.div,
            "pi": self.pi,
            "e": self.e,
            "sq": self.sq,
            "sqrt": self.sqrt,
            "pow": self.pow,
            "sin": self.sin,
            "asin": self.asin,
            "ln": self.ln,
            "exp": self.exp,
        }
        self.helptext = '''
Stack:
   number - push, p - pop, c - clear, d - duplicate, w - swap
Arithmetic:
   + - * /   ('x' is the same as '*')
Constants:
   pi, e
Functions (most from Python math):
   sq, sqrt, pow, sin, asin, ln, exp
'''
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
    def swap(self):
        x = self.stack.pop()
        y = self.stack.pop()
        self.stack.append(x)
        self.stack.append(y)
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
    def sin(self):
        x = self.pop()
        if self.degrees:
            x = math.radians(x)
        n = math.sin(x)
        self.stack.append(n)
        return n
    def asin(self):
        n = math.asin(self.pop())
        if self.degrees:
            n = math.degrees(n)
        self.stack.append(n)
        return n
    def ln(self):
        n = math.log(self.pop())
        self.stack.append(n)
        return n
    def exp(self):
        n = math.exp(self.pop())
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
