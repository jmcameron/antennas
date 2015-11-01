"""
TESTS FOR LOOP

>>> from loop import Loop

Try a test from the www.66pacific.com calculator
------------------------------------------------

>>> a = Loop('octagon', 9.0, 14.0, 0.9, 100.0)

>>> print(a.summary())
Loop antenna shape: octagon
   Conductor length: 9.000 feet
   Conductor diameter: 0.900 inches
   Segment length: 1.125 feet
   Loop area: 6.111 square feet
   Loop diameter: 2.716 feet
Operating frequency: 14.000 MHz
Loss resistance: 0.0373 ohms
Radiation resistance: 0.0485 ohms
Inductance: 2.033 henrys
Inductive reactance: 178.805 ohms
Tuning capacitance: 63.579 pF
Capacitor voltage: 4317.5 volts
Distributed capacity: 7.380 pF
Antenna bandwidth: 13.429 kHz
Quality Factor (Q): 1042.51
Efficiency: 56.5 %

NOTE: This does not correspond exactly to the loop calculator on 
      http://www.66pacific.com/calculators/small_tx_loop_calc.aspx
      Not sure if there is a problem or not.  But it is close.  The
      differences may be to approximations by Hart for octagons?

      Using the parameters above and setting the shape to a circle, these
      equations duplicate the Excel spreadsheet created by Steve Yates, which
      is available at: http://www.aa5tb.com/loop.html


Now adjust a couple of things and try another test

>>> a.s = 12.0
>>> a.f = 10.0

>>> print(a.summary())
Loop antenna shape: octagon
   Conductor length: 12.000 feet
   Conductor diameter: 0.900 inches
   Segment length: 1.500 feet
   Loop area: 10.864 square feet
   Loop diameter: 3.621 feet
Operating frequency: 10.000 MHz
Loss resistance: 0.0420 ohms
Radiation resistance: 0.0399 ohms
Inductance: 2.920 henrys
Inductive reactance: 183.451 ohms
Tuning capacitance: 86.756 pF
Capacitor voltage: 4533.1 volts
Distributed capacity: 9.840 pF
Antenna bandwidth: 8.927 kHz
Quality Factor (Q): 1120.14
Efficiency: 48.7 %

"""

if __name__ == "__main__":
    import doctest
    doctest.testmod()
