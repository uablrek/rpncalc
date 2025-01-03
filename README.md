# A comand-line RPN calculator in Python

A minimalistic comand-line [Reverse Polish Notation](
https://en.wikipedia.org/wiki/Reverse_Polish_notation) calculator.

Most open-source RPN calculators are graphic replicas of old HP
calculators. They look great, and as I studied in 1990s, I am a fan of
HP calculators. But my needs are simpler and I want to use the
keyboard (only). There are command-line RPN calculators available
e.g. `dc`, but they have irritating limitations, or are too hard
to adapt.

I wanted a super-simple keyboard RPN calculator that could *easily* be
extended/adapted to my needs.

Help text (at the moment of writing):
```
> ./rpncalc.py h
Stack:
   number - push, p - pop, c - clear, d - duplicate, w - swap
Arithmetic:
   + - * /   ('x' is the same as '*')
Constants:
   pi, e
Functions (most from Python math):
   neg, sq, sqrt, pow, sin, asin, ln, exp

UI functions:
   q, ctrl-D - Quit
   h - Help
   hc - Print constants
   = - Print top-of-stack (top)
   s, (empty) - Print stack
   eng - Print top in engineering style
   si - Toggle si-prefix or exponent for "eng"
   prec - Precision for "eng". Significant digits from top
   deg - Angles are in degrees
   rad - Angles are in radians
   hex - Print top as hexa-decimal
   time - Print top as time (duration)
```

Example:
```
./rpncalc.py h   # help
./rpncalc.py hc  # Print extra constants (beside pi and e)
# Volume of earth R=6378km, V=4/3*pi*r^3
./rpncalc.py '4 3 / pi * 6378 3 pow *'  # (in km3)
1086781292542.8892
# (note that the string is quoted to prevent the shell from expanding '*')
# Or using 'x' and constants (no quotes needed)
./rpncalc.py 4 3 / pi x Re 3 pow x eng # (in m3)
1.087e21
# Interactive:
./rpncalc.py
(0) > 4 3 /
1.3333333333333333
(1) > pi *
4.1887902047863905
(1) > Re 3 pow
2.59449922152e+20
(2) > *
1.0867812925428892e+21
(1) > si eng
1.087Z
```

`si eng` to get [si prefix representation](
https://en.wikipedia.org/wiki/Metric_prefix). So the volume of earth is
1.087 Zm<sup>3</sup> 

Recipes:
```
alias rc="$PWD/rpncalc.py"
rc pi =                           # Print pi
rc 0xffc =                        # Hex -> decimal
rc 4092 hex                       # Decimal -> hex
rc 50 1 w /                       # 1/50, invert top with "1 w /"
rc 3 prec 1086781292542.8 eng     # Volume of earth in km3 with 3 digits
rc 20 5 x                         # Use 'x' instead of '*' (no shell expansion)
rc au C / time                    # Time for sunlight to reach Earth
rc Re sq g x G / eng              # Mass of Earth (kg)
rc Ls au sq pi x 4 x / eng        # Solar power per m2 (W/m2) at Earth distance
rc Dm 100 3.6 / / time            # Time to drive to the moon at 100 km/h
rc -18 Z -                        # -18 degrees Celsius in degrees Kelvin
rc kcal 1e12 x eng                # One Megaton of energy in J
rc kcal 1e9 x 15 x si eng         # A Hiroshima bomb (15 kiloton)
```

## Constants

Beside the mathematical constants, `pi` and `e`, other (physical)
constants can be defined. Constants are read from json files, by
default [constants.json](constants.json). If `$RPNCALC_PATH` is
specified, all "*.json" files in those directories are loaded.

Since I use `rpncalc` for energy and astronomical computations,
default constants are in that area.

```
./rpncalc.py hc
sb - Stefan–Boltzmann constant (W/m2/K^4): 5.67e-08
Re - Radius Earth (m): 6378000.0
Rs - Radius Sun (m): 696340000.0
au - Astronomical Unit (m): 149597870700
C - Speed of light (m/s): 299792458
G - Gravitational constant (N*m2/kg2): 6.6743e-11
g - Gravity of Earth (m/s2): 9.80665
ly - Light year (m): 9460730472580800
Dm - Distance to the moon (m): 384400000
btu - British Thermal Unit (J): 1055.1
kcal - Kilocalorie (J): 4184
kwh - kWh (J): 3600000.0
Ls - Solar Luminosity (W): 3.828e+26
Z - Absolute Zero temperature (Celsius): -273.15
mev - MeV Mega Electron Volt (J): 1.6e-13
```

**Warning:** there is no check for conflicts or errors when loading
constants


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

This is not a bug, and it will not be fixed.  If it's good enough
for Python, it's good enough for me.


## Implementation

Implementation consists of two parts:

1. [The calculator](rpn.py). The stack and core functions
2. [The User Interface](rpncalc.py). Calls the calculator and add non-math
   functions, like print functions, and physical constants

The calculator passes all exceptions to the caller. I.e. no exceptions
are caught or raised by the calculator. This is intentional.

New math functions are added to the calculator (e.g. trig), while
functions like printouts or modes (deg/rad), and constants are added to
the UI.

The calculator must always be possible to test with unit-tests.
```
python -m unittest discover
```


# Contributions and maintenance

Issues/PRs are welcome. But please note that the intention is to keep
it simple. I will add things I need when I need them, and add some
functions just for fun.

I have refrained from adding some "memory" function, even though it
would be simple. A bit of a point with RPN is to *not* need memories.
