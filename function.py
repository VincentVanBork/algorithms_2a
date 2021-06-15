import numpy as np
from numpy import abs, cos, exp, mean, pi, prod, sin, sqrt, sum


def rosenbrock(x):  # rosen.m
    """ http://en.wikipedia.org/wiki/Rosenbrock_function """
    # a sum of squares, so LevMar (scipy.optimize.leastsq) is pretty good
    x = np.asarray_chkfinite(x)
    x0 = x[:-1]
    x1 = x[1:]
    return sum((1 - x0) ** 2) + 10 * sum((x1 - x0 ** 2) ** 2)

def ackley(x):
    a = 20
    b = 0.2
    c = 2 * pi
    x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
    n = len(x)
    s1 = sum(x ** 2)
    s2 = sum(cos(c * x))
    return -a * exp(-b * sqrt(s1 / n)) - exp(s2 / n) + a + exp(1)
