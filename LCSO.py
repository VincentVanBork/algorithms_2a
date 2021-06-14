import random

import numpy as np

from function import rosenbrock
from numpy.random import default_rng


class Swarm:
    def __init__(self,
                 population_number, dimensions, num_sub_swarms,
                 domain,
                 function):
        self.num_sub_swarms = num_sub_swarms
        self.function = function
        self.dimensions = dimensions
        self.particles: list[Particle] = []
        self.domain = domain
        for i in range(population_number):
            self.particles.append(Particle(i, dimensions))
        self._initialize_positions(self.domain)
        self._divide_into_sub_swarms()
        self._update_values()

    def _update_values(self):
        for particle in self.particles:
            particle.update_current_value(self.function)

    def _initialize_positions(self, domain):
        for particle in self.particles:
            particle.position = particle.position * (domain[1] - domain[0]) + \
                                domain[0]

    def _divide_into_sub_swarms(self):
        sub_swarm_id = 1
        for particle in self.particles:
            particle.sub_swarm_id = sub_swarm_id
            sub_swarm_id += 1
            if sub_swarm_id > self.num_sub_swarms:
                sub_swarm_id = 1

    def _update_second_place(self, second, winner):
        rng = default_rng()
        r1, r2 = rng.random(2)
        self.particles[second.id].velocity = \
            r1 * second.velocity + \
            r2 * (winner.position - second.position)
        self.particles[second.id].position = \
            second.position + self.particles[second.id].velocity

    def _update_third_place(self, third, second, winner):
        rng = default_rng()
        r1, r2, r3 = rng.random(3)
        self.particles[third.id].velocity = \
            r1 * third.velocity + \
            r2 * (winner.position - third.position) + \
            r3 * (second.position - third.position)
        self.particles[third.id].position = \
            third.position + self.particles[third.id].velocity

    def sub_swarm_tournaments(self):
        for sub_swarm in range(self.num_sub_swarms):
            sub_swarm_id = sub_swarm + 1
            # print(sub_swarm_id)
            sub_swarm_particles = [
                particle.id for particle in self.particles
                if
                (particle.sub_swarm_id == sub_swarm_id and
                 particle.place == 0)
            ]

            remaining_particles = [
                particle.place
                for particle in self.particles
                if particle.sub_swarm_id == sub_swarm_id
            ]

            while remaining_particles.count(0) >= 3:

                players = random.sample(sub_swarm_particles, 3)

                contestants = [self.particles[player] for player in players]
                winners = sorted(contestants, key=lambda x: x.current_value)
                for podium, winner in enumerate(winners):
                    self.particles[winner.id].place = podium + 1

                self._update_second_place(winners[1], winners[0])
                self._update_third_place(winners[2], winners[1], winners[0])

                remaining_particles = [
                    particle.place
                    for particle in self.particles
                    if particle.sub_swarm_id == sub_swarm_id]

                sub_swarm_particles = [
                    particle.id for particle
                    in self.particles
                    if (particle.sub_swarm_id == sub_swarm_id and
                        particle.place == 0)
                ]

            self._update_values()

    def _clear_winners(self):
        for particle in self.particles:
            particle.position = 0

    def whole_swarm_tournament(self):
        winners_particles = [
            particle.id for particle
            in self.particles
            if particle.place == 1
        ]

        while len(winners_particles) >= 3:

            players = random.sample(winners_particles, 3)

            contestants = [self.particles[player] for player in players]
            winners = sorted(contestants, key=lambda x: x.current_value)

            for podium, winner in enumerate(winners):
                self.particles[winner.id].place = 0

            self._update_second_place(winners[1], winners[0])
            self._update_third_place(winners[2], winners[1], winners[0])

            winners_particles = [
                particle.id for particle
                in self.particles
                if particle.place == 1
            ]

        self._update_values()
        self._clear_winners()


class Particle:
    def __init__(self, particle_id, dimensions):
        self.sub_swarm_id: int = 0
        self.id: int = particle_id
        self.position = np.random.rand(dimensions)
        self.velocity = np.random.rand(dimensions)
        self.place = 0
        self.current_value = np.inf

    def update_current_value(self, function):
        self.current_value = function(self.position)

    def __str__(self):
        return f"{self.id}_{self.current_value}"


if __name__ == "__main__":
    s = Swarm(population_number=6,
              dimensions=20,
              num_sub_swarms=2,
              domain=(-2.048, 2.048),
              function=rosenbrock)
    for i in range(2):
        print(i)
        s.sub_swarm_tournaments()
        s.whole_swarm_tournament()
        print(min([particle.current_value for particle in s.particles]))