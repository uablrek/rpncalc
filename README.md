# A comand-line RPN calculator in Python

A minimalistic comand-line [Reverse Polish Notation](
https://en.wikipedia.org/wiki/Reverse_Polish_notation) calculator.

Most open-source RPN calculators are graphic replicas of old HP
calculators. They look great, and as I studied in 1990s, I am a fan of
HP calculators. But my needs are simpler and I want to use the
keyboard (only). There are comand-line RPN calculators available
e.g. `dc`, but they have irritating minor limitations, or too many
bells-and-whistles.

I wanted a super-simple keyboard RPN calculator that could *easily* be
extended/adapted to my needs.

Help text (at the moment of writing):
```
> ./rpncalc.py h

Stack:
   number - push, p - pop, c - clear, d - duplicate, w - swap
Arithmetic:
   + - * /
Constants:
   pi e
Functions (most from Python math):
   sq, sqrt, pow, sin

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
```

Example:
```
./rpncalc.py h  # help
# Volume of earth R=6378km, V=4/3*pi*r^3
./rpncalc.py '4 3 / pi * 6378 3 pow *'
1086781292542.8892
# (note that the string is quoted to prevent the shell from expanding '*')
# Interactive (in si units/prefix):
./rpncalc.py
(0) > 4 3 /
1.3333333333333333
(1) > pi *
4.1887902047863905
(1) > 6378e3 3 pow
2.59449922152e+20
(2) > *
1.0867812925428892e+21
(1) > eng
1.0868Z
```

`eng` to get [si prefix representation](
https://en.wikipedia.org/wiki/Metric_prefix). So the volume of earth is
1.0868 Zm<sup>3</sup> 

Recipes:
```
alias rc="$PWD/rpncalc.py"
rc pi =                           # Print pi
rc 0xffc =                        # Hex -> decimal
rc 4092 hex                       # Decimal -> hex
rc si 3 prec 1086781292542.8 eng  # Volume of earth in km3 with 3 digits
rc 20 5 x                         # Use 'x' instead of '*' (no shell expansion)
```

## Key-pad comma

In many keyboard layouts the Key-pad with "numlock" print a comma
`,`. To remap to a dot do:

```
setxkbmap se -option kpdl:dot
```
(switch "se" to your layout)


## Standard Python arithmetic

This means that "strange things" are inherited, like numbers that do
not have exact representations in binary floating point (see the
[decimal package](https://docs.python.org/3/library/decimal.html)).

```
> ./rpncalc.py 1.1 2.2 +
3.3000000000000003
```

This is not a bug, and it will not be "fixed".  If it's good enough
for Python, it's good enough for me.


## Implementation

Implementation consists of two parts:

1. [The calculator](rpn.py). The stack and core functions
2. [The User Interface](rpncalc.py). Calls the calculator and add non-math
   functions like `eng` and "print-stack"

The calculator passes all exceptions to the caller. I.e. no exceptions
are caught or raised by the calculator. This is intentional.

New math functions are added to the calculator (e.g. trig), while
functions like nice printouts or save/restore are added to the UI.

The calculator must always be possible to test with unit-tests.
```
python -m unittest discover
```


# Contributions and maintenance

Issues/PRs are welcome. But please note that the intention is to keep
it simple. I will add things I need when I need them, and perhaps add
some functions just for fun.
