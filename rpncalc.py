#! /usr/bin/python

import rpn
import sys
import math
import datetime
import readline
import json
import os
import pathlib

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
        self.si = False
        self.format = "%.4g"
        self.cmd = {
            "q": exit,
            "h": self.help,
            "hc": self.print_constants,
            "hcj": self.print_constants_json,
            "=": self.top,
            "s": self.stack,
            "eng": self.eng,
            "si": self.tsi,
            "prec": self.prec,
            "deg": self.deg,
            "rad": self.rad,
            "hex": self.hex,
            "time": self.time,
        }
        self.helptext = '''
UI functions:
   q, ctrl-D - Quit
   h - Help
   hc - Print constants
   hcj - Print constants in json
   = - Print top-of-stack (top)
   s, (empty) - Print stack
   eng - Print top in engineering style
   si - Toggle si-prefix or exponent for "eng"
   prec - Precision for "eng". Significant digits from top
   deg - Angles are in degrees
   rad - Angles are in radians
   hex - Print top as hexa-decimal
   time - Print top as time (duration)
'''
        self.constants = {}
        if "RPNCALC_PATH" in os.environ:
            self.constants = {}
            for d in os.environ["RPNCALC_PATH"].split(os.pathsep):
                self.load_constants(d)
        else:
            self.load_constants(pathlib.Path(__file__).resolve().parent)

    def load_constants(self, d):
        for f in pathlib.Path(d).glob('*.json'):
            with open(f, 'r') as file:
                self.constants = self.constants | json.load(file)

    def help(self):
        print(self.c.helptext, end='')
        print(self.helptext)
    def print_constants(self):
        for k,v in self.constants.items():
            print(f"{k} - {v[1]}: {v[0]}")
    def print_constants_json(self):
            print(json.dumps(self.constants))
    def eval(self, str):
        for t in str.split():
            r = None
            if t in self.cmd:
                self.cmd[t]()
            elif t in self.constants:
                self.c.push(self.constants[t][0])
            else:
                r = self.c.exec(t)
        return r

    def top(self):
        if len(self.c.stack) == 0:
            raise IndexError("Stack empty")
        print(self.c.top())
    def stack(self):
        for i in self.c.stack:
            print(i)
    def eng(self):
        if len(self.c.stack) == 0:
            raise IndexError("Stack empty")
        print(eng_string(self.c.top(), format=self.format, si=self.si))
    def tsi(self): # (toggle si)
        self.si = not self.si
    def prec(self):
        if len(self.c.stack) == 0:
            raise IndexError("Stack empty")
        x = self.c.pop()
        self.format = f"%.{x}g"
    def deg(self):
        self.c.degrees = True
    def rad(self):
        self.c.degrees = False
    def hex(self):
        if len(self.c.stack) == 0:
            raise IndexError("Stack empty")
        print(hex(self.c.top()))
    def time(self):
        if len(self.c.stack) == 0:
            raise IndexError("Stack empty")
        t = round(self.c.top())
        print(datetime.timedelta(seconds=t))

if __name__ == "__main__":
    c = rpncalc()
    if len(sys.argv) > 1:
        try:
            r = None
            for t in sys.argv[1:]:
                r = c.eval(t)
            if r:
                print(r)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
        exit()
    while True:
        try:        
            line = input(f"({len(c.c.stack)}) > ")
            if not line or line.isspace():
                c.stack()
            else:
                r = c.eval(line)
                if r:
                    print(r)
        except (EOFError, SystemExit):
            sys.exit(0)   # Is there another way?
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
