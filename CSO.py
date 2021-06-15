import os
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


class Swarm:
    def __init__(self,
                 population_number, influence_coefficient,
                 function,
                 dimensions, domain):
        self.influence_coefficient = influence_coefficient
        self.average_position = None

        self.positions = np.empty((population_number, dimensions))
        self.velocities = np.empty((population_number, dimensions))

        self.population_number = population_number
        self.function = function

        self.values = None
        self.winners = np.zeros(self.population_number, dtype=bool)
        self.particles = None

        self.domain = domain
        self.dimensions: int = dimensions

    def initialize_swarm(self):
        self.velocities = np.random.rand(
            self.population_number, self.dimensions)

        self.positions = np.random.rand(self.population_number,
                                        self.dimensions)
        self.positions = self.positions * (self.domain[1] - self.domain[0]) + \
                         self.domain[0]
        self.particles = np.dstack((self.positions, self.velocities))

        self.update_average_position()
        self.update_values()

    def iterate(self):
        self.tournament()
        # self.update_velocities()
        # self.update_positions()
        self.update_average_position()
        self.update_values()

    def update_values(self):
        self.values = np.apply_along_axis(self.function, 1,
                                          self.particles[:, :, 0])

    def update_average_position(self):
        self.average_position = np.mean(self.particles[:, :, 0], axis=0)

    def tournament(self):
        self.winners.fill(0)
        aleph_fighters = np.random.choice(range(self.population_number),
                                          size=int(self.population_number / 2),
                                          replace=False)
        bet_fighters = np.array([value for value in
                                 range(self.population_number) if
                                 value not in aleph_fighters])
        # print(self.winners)
        # print("alpha", aleph_fighters)
        # print("beta", bet_fighters)
        for alpha, beta in zip(aleph_fighters, bet_fighters):
            # print("|||||||||||||")
            # print(alpha, beta)
            if self.values[alpha] < self.values[beta]:
                self.winners[alpha] = True
                self.particles[beta] = self.update_velocity(
                    particle=self.particles[beta],
                    winner=self.particles[alpha],
                )

                self.particles[beta] = self.update_position(
                    self.particles[beta])
                # print("updated position")
                # print(self.particles[beta])
            else:
                self.winners[beta] = True
                self.particles[alpha] = self.update_velocity(
                    particle=self.particles[alpha],
                    winner=self.particles[beta],
                )

                self.particles[alpha] = self.update_position(
                    self.particles[alpha])
                # print("updated position")
                # print(self.particles[alpha])

        # print(self.winners)

    def update_velocity(self, particle, winner):
        rng = default_rng()
        r1, r2, r3 = rng.random(3)
        # print(r1, r2, r3)
        # print(particle)
        # print(particle[:, 1])
        particle[:, 1] = (r1 * particle[:, 1]) + \
                         (r2 * (winner[:, 0] - particle[:, 0])) + \
                         (self.influence_coefficient * r3 * (
                                 self.average_position -
                                 particle[:, 0]))
        # print("________")
        # print(particle)
        return particle

    def update_position(self, particle):
        particle[:, 0] = particle[:, 0] + particle[:, 1]
        for i in range(s.dimensions):
            if particle[i, 0] > s.domain[1]:
                particle[i, 0] = s.domain[1]
            elif particle[i, 0] < s.domain[0]:
                particle[i, 0] = s.domain[0]

        return particle


if __name__ == "__main__":
    # swarms = []
    # num_of_swarms = 5
    # for i in range(num_of_swarms):
    #     swarms.append(
    #         Swarm(population_number=100, influence_coefficient=0,
    #               function=rosenbrock, dimensions=30,
    #               domain=(-2.048, 2.048)))
    # for swarm in swarms:
    #     swarm.initialize_swarm()
    #     swarm.update_average_position()
    #
    global whole_swarm_position
    global sub_swarms

    sub_swarms = []
    whole_swarm_position = []
    num_of_sub_swarms = 4
    test_population_number = int(160 /num_of_sub_swarms)
    for i in range(num_of_sub_swarms):
        s = Swarm(population_number=test_population_number, influence_coefficient=0.3,
                  function=ackley, dimensions=30,
                  domain=(-32, 32))
        s.initialize_swarm()
        s.update_average_position()

        sub_swarms.append(s)

    all_particles = np.concatenate(tuple(subs.particles for subs in sub_swarms))

    whole_swarm_position = np.mean(all_particles[:, :, 0], axis=0)

    # plt.show()
    # print(s.particles)
    # print(s.particles[:, :, 0])
    # print(s.particles[:, :, 0])
    """----------------------------"""
    # fig, ax = plt.subplots()
    # scatter = ax.scatter(x=s.particles[:, 0, 0], y=s.particles[:, 1, 0])
    #
    # def update_scatter(i):
    #     s.iterate()
    #     scatter.set_offsets(s.particles[:, :, 0])
    #     return scatter,

    # anim = FuncAnimation(fig, update_scatter, interval=300, frames=100)
    # anim.save('CSO_rosenbrock.gif')
    # plt.show()

    """----------------------------"""

    fig_bar, ax_bar = plt.subplots()

    # print(*all_values)
    merged_all_values = np.concatenate(tuple(subs.values for subs in sub_swarms))
    bar = ax_bar.bar(x=range(len(merged_all_values)), height=merged_all_values)


    def update_bar(i):
        global whole_swarm_position
        global sub_swarms
        # print(f" iteration {i}")
        for sub_swarm in sub_swarms:
            sub_swarm.iterate()

        all_particles = np.concatenate(tuple(subs.particles for subs in sub_swarms))
        whole_swarm_position = np.mean(all_particles[:, :, 0], axis=0)
        print("WHOLE SWARM AVERAGE:", rosenbrock(whole_swarm_position))

        merged_all_values = np.concatenate(tuple(subs.values for subs in sub_swarms))

        ax_bar.set_ylim(top=max(merged_all_values))
        for i in range(len(bar)):
            bar[i].set_height(merged_all_values[i])
        return ax_bar,


    anim = FuncAnimation(fig_bar, update_bar, interval=300, frames=300,
                         repeat=False)
    anim.save(f'CSO_rosenbrock_values_test_{num_of_sub_swarms}_{test_population_number}.mp4', writer=FFMpegWriter(),
              progress_callback=lambda i, n: print(f"frame {i} of {n}"))
    # plt.show()

    """----------------------------"""

    # fig_hist, ax_hist = plt.subplots()
    # n_bins = int(s.population_number / 5) if int(
    #     s.population_number / 5) > 10 else 10
    # hist, _, bar_container = ax_hist.hist(s.values, bins=n_bins)
    #
    #
    # def update_hist(i):
    #
    #     s.iterate()
    #     # ax_hist.set_ylim(top=max(s.values))
    #     n, _ = np.histogram(s.values, n_bins)
    #     for count, rect in zip(n, bar_container.patches):
    #         rect.set_height(count)
    #     return bar_container.patches
    #
    #
    # anim = FuncAnimation(fig_hist, update_hist, interval=100, save_count=1000,
    #                      repeat=False)
    # anim.save('CSO_rosenbrock_histogram.mp4', writer=FFMpegWriter(),
    #           progress_callback=lambda i, n: print(f"frame {i} of {n}"))
    # plt.show()

    """________________________"""
