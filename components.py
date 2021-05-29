import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from function import rosenbrock
from numpy.random import default_rng


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

        self.positions = np.random.randint(self.domain[0], self.domain[1],
                                           size=(self.population_number,
                                                 self.dimensions))
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

        print(self.winners)

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

        # r1, r2, r3 = np.random.choice(, replace = False, size(3))
        #     self.velocity

    def update_position(self, particle):
        particle[:, 0] = particle[:, 0] + particle[:, 1]
        return particle

    # def update_velocity(self, winner_position, average_position,
    #                     influence_coefficient):
    #

    # class Particle:
    #     def __init__(self, dimension, low, high):
    #         self.position = np.random.randint(low, high, size=dimension)
    #         self.velocity = np.random.rand(dimension)
    #
    #     def update_velocity(self, winner_position, average_position,
    #     influence_coefficient):
    #         r1, r2, r3 = np.random.rand(3)
    #         self.velocity = (r1 * self.velocity) + \
    #                         (r2 * (winner_position - self.position)) + \
    #                         (influence_coefficient * r3 * (average_position -
    #                         self.position))


if __name__ == "__main__":
    s = Swarm(population_number=6, influence_coefficient=0,
              function=rosenbrock, dimensions=2,
              domain=(-100, 100))
    s.initialize_swarm()
    s.update_average_position()
    for i in range(100):
        s.iterate()
    print(s.particles)
    # print(s.average_position)
    # s.tournament()
    # print(s.particles[1])
    # print(s.particles)
    # print(s.particles[:, :, 0])
    # for sth in s.particles[:, :, 0]:
    #     print(sth)
    #     print(rosenbrock(sth))
    # print(s.values)
    # print(s.particles[:, :, 0])
    # print(np.mean(s.particles[:, :, 0], axis=0))
