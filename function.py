import numpy as np


def rosenbrock(x):  # rosen.m
    """ http://en.wikipedia.org/wiki/Rosenbrock_function """
    # a sum of squares, so LevMar (scipy.optimize.leastsq) is pretty good
    x = np.asarray_chkfinite(x)
    x0 = x[:-1]
    x1 = x[1:]
    return sum((1 - x0) ** 2) + 10 * sum((x1 - x0 ** 2) ** 2)
