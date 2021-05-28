import numpy as np


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

        self.domain = domain
        self.dimensions = dimensions

    def initialize_swarm(self):
        for index, value in enumerate(range(self.population_number)):
            self.positions[index] = np.random.randint(self.domain[0],
                                                      self.domain[1],
                                                      size=self.dimensions)
            self.velocities[index] = np.random.rand(self.dimensions)

        self.update_average_position()

    def iterate(self):
        ...

    def update_average_position(self):
        self.average_position = np.mean(self.positions, axis=0)

    def tournament(self):
        ...


    # def update_velocity(self, winner_position, average_position,
    #                     influence_coefficient):
    #     r1, r2, r3 = np.random.rand(3)
    #     self.velocity = (r1 * self.velocity) + \
    #                     (r2 * (winner_position - self.position)) + \
    #                     (influence_coefficient * r3 * (average_position -
    #                                                    self.position))


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
    s = Swarm(population_number=10, influence_coefficient=0,
              function=lambda x: x, dimensions=5,
              domain=(-5, 5))
    s.initialize_swarm()
    s.update_average_position()
    print(s.average_position)
    s.tournament()
