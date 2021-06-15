import copy
import os
import random

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation, FFMpegWriter

matplotlib.use('tkagg')
from function import rosenbrock, ackley
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
                 function,
                 switcheroo_probability,
                 power_over_whelming,
                 sensor_overload,
                 increment_for_a,
                 max_a
                 ):

        self.p = switcheroo_probability
        self.a = power_over_whelming
        self.c = sensor_overload
        self.increment = increment_for_a
        self.max_a = max_a

        self.function = function
        self.dimensions = dimensions
        self.butts: list[Butterfly] = []
        self.domain = domain
        for i in range(population_number):
            self.butts.append(Butterfly(i, dimensions))
        self._initialize_positions(self.domain)
        self._update_values()
        self.best_butt = min(self.butts, key=lambda b: b.stimulus_intensity)
        self.template = copy.deepcopy(self.butts)

    def _update_values(self):
        for butte in self.butts:
            for i in range(self.dimensions):
                if butte.position[i] > self.domain[1]:
                    butte.position[i] = self.domain[1]
                elif butte.position[i] < self.domain[0]:
                    butte.position[i] = self.domain[0]

        for butte in self.butts:
            butte.calculate_stimulus(self.function)

    def _initialize_positions(self, domain):
        for butte in self.butts:
            butte.position = butte.position * (domain[1] - domain[0]) + \
                             domain[0]

    def find_best_butt(self):
        self.best_butt = min(self.butts, key=lambda b: b.stimulus_intensity)
        return self.best_butt

    def _calculate_whole_fragrance(self):
        for butte in self.butts:
            butte.calculate_fragrance(self.c, self.a)

    def _cross_and_mutate_butter(self):
        ...
        for id_b, butte in enumerate(self.template):
            bk = random.choice(self.template)
            while butte.id != bk.id:
                bk = random.choice(self.template)
            if butte.stimulus_intensity < bk.stimulus_intensity:
                butte.fragrance *= random.random()
                # butte.calculate_stimulus(self.function)
            else:
                butte.fragrance = bk.fragrance

            mutated_position = np.random.rand(self.dimensions)
            mutated_position = mutated_position * (
                    self.domain[1] - self.domain[0]) + self.domain[0]
            if self.function(butte.position) > self.function(mutated_position):
                butte.position = mutated_position
                # butte.global_search(self.find_best_butt())

            best_butt = min(self.template,
                            key=lambda b: self.function(b.position))
            print("BEST", best_butt.stimulus_intensity)
            size_of_butts = len(self.template)
            if random.random() < self.p or id_b in [size_of_butts - 1,
                                                    size_of_butts - 2]:
                butte.global_search(best_butt, self.template[id_b])
            else:
                butte.local_search(self.butts[id_b + 1],
                                   self.butts[id_b + 2])

            # butte.global_search(best_butt, butte)
            for i in range(self.dimensions):
                if butte.position[i] > self.domain[1]:
                    butte.position[i] = self.domain[1]
                elif butte.position[i] < self.domain[0]:
                    butte.position[i] = self.domain[0]

            butte.calculate_stimulus(self.function)
            # butte.calculate_fragrance(self.c, self.a)

    def _increment_power_coeff(self):
        if self.a > self.max_a:
            self.a = self.max_a
        else:
            self.a += self.increment

    def fly_the_butts(self):
        self._calculate_whole_fragrance()
        best_butt = self.find_best_butt()
        # best_butt = min(self.template, key=lambda b: self.function(b.position))
        for id_b, butte in enumerate(self.butts):
            r = random.random()
            size_of_butts = len(self.butts)
            if random.random() < self.p or id_b in [size_of_butts - 1,
                                                    size_of_butts - 2]:
                butte.global_search(best_butt, self.template[id_b])
            else:
                bk = random.choice(self.butts)
                bk2 = random.choice(self.butts)
                butte.local_search(bk, bk2)
                # butte.local_search(self.butts[id_b + 1],
                #                    self.butts[id_b + 2])
        self._update_values()
        self._increment_power_coeff()
        self._cross_and_mutate_butter()


class Butterfly:
    def __init__(self, b_id, dim):
        self.id = b_id
        self.position = np.random.rand(dim)
        self.fragrance: float = 0
        self.stimulus_intensity: float = 0

    def calculate_stimulus(self, function):
        self.stimulus_intensity = function(self.position)

    def calculate_fragrance(self, c, a):
        self.fragrance = c * (self.stimulus_intensity ** a)

    def global_search(self, best, template):
        r = random.random()
        # TODO: stimulus_intensity vs position of best
        self.position = \
            self.position + \
            (((
                          r ** 2) * best.stimulus_intensity) - self.position) * self.fragrance
        # self.position = random.random() * self.position

    def local_search(self, after, afterparty):
        r = random.random()
        self.position = \
            self.position + \
            (
                    (r ** 2) * after.position - afterparty.position
            ) * self.fragrance


if __name__ == "__main__":
    iters = 100
    population_num = 50
    dimensioneses = 30
    min_a = 0.1
    max_a = 0.3
    s = MurderousButterflySwarm(
        population_number=population_num, dimensions=dimensioneses,
        domain=(-32, 32),
        function=ackley,
        switcheroo_probability=0.8,
        power_over_whelming=0.01,
        sensor_overload=min_a,
        increment_for_a=((max_a - min_a) / iters),
        max_a=max_a
    )
    print("POP NUM", population_num)
    print("DIM", dimensioneses)
    print("functeion", s.function.__name__)
    print("MAX_A", s.max_a)
    print("INCREMENT", s.increment)
    print("START A", s.a)
    print("SWITCH", s.p)
    fig_bar, ax_bar = plt.subplots()
    heights = [p.stimulus_intensity for p in s.butts]
    bar = ax_bar.bar(x=range(len(s.butts)),
                     height=heights)
    values = [1]


    def update_bar(i):
        s.fly_the_butts()
        values = sorted([p.stimulus_intensity for p in s.butts])
        ax_bar.set_ylim(top=sum(values) / len(values))
        ax_bar.set_title(f"Frame of {i}")
        # print(values)
        for i in range(len(bar)):
            bar[i].set_height(values[i])
        return ax_bar,


    anim = FuncAnimation(fig_bar, update_bar, interval=300, frames=iters,
                         repeat=False)
    plt.show()

    # for i in range(iters):
    #     s.fly_the_butts()
    #
    print("MINIMMAL VALUE", sorted([p.stimulus_intensity for p in s.butts])[0])
    print("MINIMMAL VALUE BY FIND", s.find_best_butt().stimulus_intensity)
    print("VALUE FROM POSITION", s.function(s.find_best_butt().position))
    print("POSITION", s.find_best_butt().position)
    values = [s.function(butt.position) for butt in s.butts]
    print("AVERAGE", sum(values) / len(values))
