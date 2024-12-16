#! /usr/bin/python

import rpn
import sys
import math

# https://stackoverflow.com/questions/17973278/python-decimal-engineering-notation-for-mili-10e-3-and-micro-10e-6
def eng_string( x, format='%s', si=False):
    '''
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    format: printf-style string used to format the value before the exponent.

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.

    E.g. with format='%.2f':
        1.23e-08 => 12.30e-9
             123 => 123.00
          1230.0 => 1.23e3
      -1230000.0 => -1.23e6

    and with si=True:
          1230.0 => 1.23k
      -1230000.0 => -1.23M
    '''
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    exp = int( math.floor( math.log10( x)))
    exp3 = exp - ( exp % 3)
    x3 = x / ( 10 ** exp3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnμm kMGTPEZY'[int(( exp3 - (-24)) / 3)]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e%s' % exp3

    return ( '%s'+format+'%s') % ( sign, x3, exp3_text)

class rpncalc:
    def __init__(self):
        self.c = rpn.calc()
        self.si = True
        self.format = "%.5g"
        self.cmd = {
            "q": exit,
            "h": self.help,
            "t": self.top,
            "=": self.top,
            "s": self.stack,
            "eng": self.eng,
            "si": self.tsi,
            "prec": self.prec,
            "deg": self.deg,
            "rad": self.rad,
            "hex": self.hex,
        }
        self.helptext = '''
UI functions:
   q, ctrl-D - Quit
   t, = - Print top-of-stack
   s, (empty) - Print stack
   eng - Print top in engineering style
   si - Toggle si-prefix or exponent for "eng"
   prec - Precision for "eng". Significant digits from top-of-stack
   deg - Angles are in degrees
   rad - Angles are in radians
   hex - Print top as hexa-decimal
'''
    def help(self):
        print(self.c.helptext, end='')
        print(self.helptext)
    def eval(self, str):
        for t in str.split(' '):
            if t in self.cmd:
                self.cmd[t]()
                r = None
            else:
                r = self.c.exec(t)
        return r
    def top(self):
        if len(self.c.stack) > 0:
            print(self.c.top())
    def stack(self):
        for i in self.c.stack:
            print(i)
    def eng(self):
        if len(self.c.stack) > 0:
            print(eng_string(self.c.top(), format=self.format, si=self.si))
    def tsi(self): # (toggle si)
        self.si = not self.si
    def prec(self):
        x = self.c.top()
        self.format = f"%.{x}g"
    def deg(self):
        self.c.degrees = True
    def rad(self):
        self.c.degrees = False
    def hex(self):
        if len(self.c.stack) > 0:
            print(hex(self.c.top()))



if __name__ == "__main__":
    c = rpncalc()
    if len(sys.argv) > 1:
        r = None
        for t in sys.argv[1:]:
            r = c.eval(t)
        if r:
            print(r)
        exit()
    while True:
        try:        
            line = input(f"({len(c.c.stack)}) > ")
            r = c.eval(line)
            if r:
                print(r)
        except (EOFError, SystemExit):
            sys.exit(0)   # Is there another way?
        except:
            print("Error")
