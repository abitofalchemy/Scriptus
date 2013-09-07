#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from pylab import *
rate = 30.0
t = np.arange(0, 10, 1/rate)
x = np.sin(2*np.pi*4*t) + np.sin(2*np.pi*7*t) + np.random.randn(len(t))*0.2
p = 20*np.log10(np.abs(np.fft.rfft(x)))
f = np.linspace(0, rate/2, len(p))
plot(f, p)
show()
