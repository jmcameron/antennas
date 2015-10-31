"""
Implement the basic small loop antenna equations developed by Ted Hart

Using the parameters in first test in loop_test.py and setting the shape
to a circle, the formulas below duplicate the Excel spreadsheet created by
Steve Yates, which is available at: http://www.aa5tb.com/loop.html

-Jonathan Cameron, KF6RTA

2015-10-30
Copyright (c) 2015
License: GPL 2.0

"""
from __future__ import print_function


from math import sqrt, pi, log10

# The known shapes

CIRCLE = 'circle'
SQUARE = 'square'
OCTAGON = 'octagon'

KNOWN_SHAPES = (CIRCLE, SQUARE, OCTAGON)


# Some convenience functions

def kilo(v):
    return v * 1.0e3

def micro(v):
    return v * 1.0e6

def pico(v):
    return v * 1.0e12



class Loop(object):
    
    def __init__(self, shape, s, f, d, p):
        """
        @param s : conductor length, feet
        @param f : operating frequncy, MHz
        @param d : conductor diameter, inches
        @param p : transmitter power, watts
        """
        if shape not in KNOWN_SHAPES:
            raise ValueError("ERROR: '%s' is not a know loop shape!" % shape)

        self._shape = shape
        self._s = s
        self._f = f
        self._d = d
        self._p = p

        self._l = None # Leg length, feet
        self._diameter = None # Loop diameter, feet
        self._a = None # area of loop, square feet

        self.recomputeShape()


    def recomputeShape(self):
        if self._shape == CIRCLE:
            self._l = 0.0
            self._diameter = self._s / (2.0*pi)
            self._a = pi * self._diameter**2.0

        elif self._shape == SQUARE:
            self._l = self._s / 4.0
            self._diameter = self._l
            self._a = self._l**2.0
            
        elif self._shape == OCTAGON:
            self._l = self._s / 8.0
            self._diameter = self._l * (1.0 + sqrt(2.0))
            self._a = 2.0 * (1.0 + sqrt(2.0)) * self._l**2.0


    # ----------------------------------------------------------------------
    # Set up properties

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, new_shape):
        if new_shape not in KNOWN_SHAPES:
            raise ValueError("ERROR: '%s' is not a know loop shape!" % new_shape)
        self._shape = new_shape
        self.recomputeShape()

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, val):
        self._s = val
        self.recomputeShape()

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, val):
        self._f = val

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, val):
        self._d = val

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, val):
        self._p = val

    # ----------------------------------------------------------------------

    def Rr(self):
        """Radiation ressistance, ohms"""
        return 3.38e-8 * (self._f**2.0 * self._a)**2.0

    def Rl(self):
        """Loss resistance, ohms)"""
        return 9.96e-4 * sqrt(self._f) * self._s / self._d

    def L(self):
        """Inductance, henrys"""
        return 1.9e-8 * self._s*(7.353 * log10(96*self._s/(pi*self._d)) - 6.386)

    def Xl(self):
        """Inductive reactance"""
        return 2.0 * pi * self._f * self.L() * 1.0e6

    def Ct(self):
        """Tuning capacitor, farads"""
        return 1.0/(2.0 * pi * self._f * self.Xl() * 1.0e6)

    def Q(self):
        """Quality factor"""
        return self.Xl()/(2.0 * (self.Rr()  + self.Rl()))

    def efficiency(self):
        """Efficiency (0 to 1.0)"""
        return self.Rr()/(self.Rr() + self.Rl())

    def bandwidth(self):
        """Loop bandwidth, hertz"""
        return self._f * 1e6 / self.Q()

    def Cd(self):
        """Distributed capacity, pF"""
        return 0.82 * self._s

    def Vc(self):
        """Capacitor potential, volts"""
        return sqrt(self._p * self.Xl() * self.Q())

    def summary(self, indent=''):
        sum = "Loop antenna shape: %s\n" % self._shape
        sum += indent + "   Conductor length: %.3f feet\n" % self._s
        sum += indent + "   Conductor diameter: %.3f inches\n" % self._d
        if self._shape != CIRCLE:
            sum += indent + "   Segment length: %.3f feet\n" % self._l
        sum += indent + "   Loop area: %.3f square feet\n" % self._a
        sum += indent + "   Loop diameter: %.3f feet\n" % self._diameter
        sum += indent + "Operating frequency: %.3f MHz\n" % self._f
        sum += indent + "Loss resistance: %.4f ohms\n" % self.Rl()
        sum += indent + "Radiation resistance: %.4f ohms\n" % self.Rr()
        sum += indent + "Inductance: %.3f henrys\n" % micro(self.L())
        sum += indent + "Inductive reactance: %.3f ohms\n" % self.Xl()
        sum += indent + "Tuning capacitance: %.3f pF\n" % pico(self.Ct())
        sum += indent + "Capacitor voltage: %.1f volts\n" % self.Vc()
        sum += indent + "Distributed capacity: %.3f pF\n" % self.Cd()
        sum += indent + "Antenna bandwidth: %.3f kHz\n" % (self.bandwidth() * 1e-3)
        sum += indent + "Quality Factor (Q): %.2f\n" % self.Q()
        sum += indent + "Efficiency: %.1f %%" % (self.efficiency() * 100.0)
        return sum
