# Simple Unit (Python implementation)

[![example workflow](https://github.com/SamuelAndresPascal/cosmoloj-py/actions/workflows/simpleunit.yml/badge.svg)](https://github.com/SamuelAndresPascal/cosmoloj-py/actions)

[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/simpleunit/badges/version.svg)](https://anaconda.org/cosmoloj/simpleunit)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/simpleunit/badges/latest_release_date.svg)](https://anaconda.org/cosmoloj/simpleunit)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/simpleunit/badges/latest_release_relative_date.svg)](https://anaconda.org/cosmoloj/simpleunit)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/simpleunit/badges/platforms.svg)](https://anaconda.org/cosmoloj/simpleunit)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/simpleunit/badges/license.svg)](https://anaconda.org/cosmoloj/simpleunit)

[![PyPI repository Badge](https://badge.fury.io/py/simpleunit.svg)](https://badge.fury.io/py/simpleunit)

* [Standard usage](#standard-usage)
* [Operator overloading usage](#operator-overloading-usage)
* [Documentation](#documentation)

This package is the Python Reference Implementation (RI) of the Simple Unit specification. Nevertheless, it also
contains some extensions to the specification standard.

## Standard usage

The standard usage refers to methods and classes defined in the Simple Unit specification.

Usage of transformed units:

```py
from simpleunit import FundamentalUnit

m = FundamentalUnit()
km = m.scale_multiply(1000)
cm = m.scale_divide(100)
cmToKm = cm.get_converter_to(km)

cmToKm.convert(3) # 0.00003
cmToKm.inverse().convert(0.00003) # 3
```

Usage of derived units:

```py
from simpleunit import FundamentalUnit, DerivedUnit

m = FundamentalUnit()
km = m.scale_multiply(1000)

km2 = DerivedUnit(km.factor(2))
cm = m.scale_divide(100)
cm2 = DerivedUnit(cm.factor(2))
km2Tocm2 = km2.get_converter_to(cm2)

km2Tocm2.convert(3) # 30000000000
km2Tocm2.inverse().convert(30000000000) # 3
```

Usage of derived units combining dimensions:

```py
from simpleunit import FundamentalUnit, DerivedUnit

m = FundamentalUnit()
kg = FundamentalUnit()
g = kg.scale_divide(1000)
ton = kg.scale_multiply(1000)
gPerM2 = DerivedUnit(g, m.factor(-2))
km = m.scale_multiply(1000)
tonPerKm2 = DerivedUnit(ton, km.factor(-2))
cm = m.scale_divide(100)
tonPerCm2 = DerivedUnit(ton, cm.factor(-2))
gPerM2ToTonPerKm2 = gPerM2.get_converter_to(tonPerKm2)
gPerM2ToTonPerCm2 = gPerM2.get_converter_to(tonPerCm2)

gPerM2ToTonPerKm2.convert(1) # 1
gPerM2ToTonPerKm2.inverse().convert(3) # 3
gPerM2ToTonPerCm2.convert(1) # 1e-4
gPerM2ToTonPerCm2.convert(3) # 3e-10
gPerM2ToTonPerCm2.offset() # 0.0
gPerM2ToTonPerCm2.scale() # 1e-10
gPerM2ToTonPerCm2.inverse().offset() # -0.0
gPerM2ToTonPerCm2.inverse().convert(3e-10) # 3
```

Usage of temperatures (affine and linear conversions):

```py
from simpleunit import FundamentalUnit, DerivedUnit

k = FundamentalUnit()
c = k.shift(273.15)
kToC = k.get_converter_to(c)

kToC.convert(0) # -273.15
kToC.inverse().convert(0) # 273.15

# combined with other units, temperatures only keep their linear conversion part
m = FundamentalUnit()
cPerM = DerivedUnit(c, m.factor(-1))
kPerM = DerivedUnit(k, m.factor(-1))
kPerMToCPerM = kPerM.get_converter_to(cPerM)

kPerMToCPerM.convert(3) # 3
kPerMToCPerM.inverse().convert(3) # 3
```

Usage of non-decimal conversions:

```py
from simpleunit import FundamentalUnit, DerivedUnit

m = FundamentalUnit()
km = m.scale_multiply(1000.)

s = FundamentalUnit()
h = s.scale_multiply(3600.)

ms = DerivedUnit(m, s.factor(-1))
kmh = DerivedUnit(km, h.factor(-1))

msToKmh = ms.get_converter_to(kmh)

msToKmh.convert(100.) # 360
msToKmh.inverse().convert(18.) # 5
```

## Operator overloading usage

The Simple Unit Python implementation provides an extension of the base specification to overloads some language operators.

Usage of transformed units:

```py
from simpleunit import FundamentalUnit

m = FundamentalUnit()
km = m * 1000
cm = m / 100
cmToKm = cm >> km

cmToKm(3) # 0.00003
(~cmToKm)(0.00003) # 3
```

Usage of derived Units:

```py
from simpleunit import FundamentalUnit

m = FundamentalUnit()
km = m * 1000

km2 = km ** 2
cm = m / 100
cm2 = cm ** 2
km2Tocm2 = km2 >> cm2

km2Tocm2(3) # 30000000000
(~km2Tocm2)(30000000000) # 3
```

Usage of derived units combining dimensions:

```py
from simpleunit import FundamentalUnit

m = FundamentalUnit()
kg = FundamentalUnit()
g = kg / 1000
ton = kg * 1000
gPerM2 = g / m ** 2
km = m * 1000
tonPerKm2 = ton * ~km ** 2
cm = m / 100
tonPerCm2 = ton / cm ** 2
gPerM2ToTonPerKm2 = gPerM2 >> tonPerKm2
gPerM2ToTonPerCm2 = tonPerCm2 << gPerM2

gPerM2ToTonPerKm2(1) # 1
(~gPerM2ToTonPerKm2)(3) # 3
gPerM2ToTonPerCm2(1) # 1e-10
gPerM2ToTonPerCm2(3) # 3e-10
gPerM2ToTonPerCm2.offset() # 0.0
gPerM2ToTonPerCm2.scale() # 1e-10
(~gPerM2ToTonPerCm2).offset() # -0.0
(~gPerM2ToTonPerCm2)(3e-10) # 3
```

Usage of temperatures (affine and linear conversions):

```py
from simpleunit import FundamentalUnit

k = FundamentalUnit()
c = k + 273.15
kToC = k >> c

kToC(0) # -273.15
(~kToC)(0) # 273.15

# combined with other units, temperatures only keep their linear conversion part
m = FundamentalUnit()
cPerM = c / m
kPerM = k / m
kPerMToCPerM = kPerM >> cPerM

kPerMToCPerM(3) # 3
(~kPerMToCPerM)(3) # 3
```

Usage of non-decimal conversions:

```py
from simpleunit import FundamentalUnit

m = FundamentalUnit()
km = m * 1000.

s = FundamentalUnit()
h = s * 3600.

ms = m / s
kmh = km / h

msToKmh = ms >> kmh

msToKmh(100.) # 360
(~msToKmh)(18.) # 5
```

## Documentation

[Latest release](https://cosmoloj.com/mkdocs/simpleunit/latest/)

[Trunk](https://cosmoloj.com/mkdocs/simpleunit/master/)
