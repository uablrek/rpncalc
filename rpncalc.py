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

if __name__ == "__main__":
    c = rpn.calc()
    if len(sys.argv) > 1:
        for t in sys.argv[1:]:
            c.eval(t)
        print(c.top())
        exit()
    while True:
        line = input(f"({len(c.stack)}) > ")
        if line == "q":
            exit()
        if not line or line.isspace():
            for i in c.stack:
                print(i)
            continue
        if line == "t":
            if len(c.stack) > 0:
                print(c.top())
            continue
        if line == "eng":
            if len(c.stack) > 0:
                print(eng_string(c.top(), format="%.3f", si=True))
            continue
        try:
            r = c.eval(line)
            if r:
                print(r)
        except:
            print("Error")
