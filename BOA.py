import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, FFMpegWriter

matplotlib.use('tkagg')
from function import rosenbrock
from numpy.random import default_rng

path_ffmpeg = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "ffmpeg", "bin", "ffmpeg.exe")
print(path_ffmpeg)
plt.rcParams['animation.ffmpeg_path'] = path_ffmpeg

sensor_modality = 1  # c
power_exponent = 1  # a
switch_probability = 0  # p


class MurderousButterflySwarm:

    def __init__(self,
                 population_number, dimensions,
                 domain,
                 function):

        self.function = function
        self.dimensions = dimensions
        self.butts: list[Butterfly] = []
        self.domain = domain
        for i in range(population_number):
            self.butts.append(Butterfly(i, dimensions))
        self._initialize_positions(self.domain)
        self._update_values()

    def _update_values(self):
        for butte in self.butts:
            butte.calculate_stimulus(self.function)

    def _initialize_positions(self, domain):
        for butte in self.butts:
            butte.position = butte.position * (domain[1] - domain[0]) + \
                             domain[0]


class Butterfly:
    def __init__(self, b_id, dim):
        self.id = b_id
        self.position = self.position = np.random.rand(dim)
        self.fragrance: float = 0
        self.stimulus_intensity: float = 0

    def calculate_stimulus(self, function):
        self.stimulus_intensity = function(self.position)

    def calculate_fragrance(self, c, a):
        return c * (self.stimulus_intensity ** a)


if __name__ == "__main__":
    s = MurderousButterflySwarm(population_number=10, dimensions=20,
                                domain=(-2.048, 2.048),
                                function=rosenbrock)
