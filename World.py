import numpy as np
from sklearn import neighbors
import pygame

import Particle
import Parameters


class Wold:
    def __init__(self):
        self.particles = []
        self.bounds = [[[100, 400], [200, 400]]]

        self.positions = np.zeros((len(self.particles), 2))
        self.velocities = np.zeros_like(self.positions)
        self.add_particle([[10 + np.random.rand(), Parameters.DOMAIN_Y_LIM[1]]])

    def add_particle(self, position):
        p = Particle.Particle()
        self.particles.append(p)
        p.set_position(position)

        self.positions = np.concatenate((self.positions, p.get_position()), axis=0)
        self.velocities = np.concatenate((self.velocities, p.get_velocity()), axis=0)

    def update(self):

        #print("pos")
        #print(self.positions)
        #print("vel")
        #print(self.velocities)

        neighbor_ids, distances = neighbors.KDTree(self.positions).query_radius(self.positions, Parameters.SMOOTHING_LENGTH, return_distance=True, sort_results=True)

        densities = np.zeros(len(self.particles))

        for i in range(len(self.particles)):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                densities[i] += Parameters.NORMALIZATION_DENSITY\
                                * (Parameters.SMOOTHING_LENGTH ** 2 - distances[i][j_in_list] ** 2) ** 3

        pressures = Parameters.ISOTROPIC_EXPONENT * (densities - Parameters.BASE_DENSITY)

        forces = np.zeros_like(self.positions)

        neighbor_ids = [np.delete(x, 0) for x in neighbor_ids]
        distances = [np.delete(x, 0) for x in distances]

        for i in range(len(self.particles)):
            for j_in_list, j in enumerate(neighbor_ids[i]):
                forces[i] += Parameters.NORMALIZATION_PRESSURE_FORCE \
                             * (-(self.positions[j] - self.positions[i]) / distances[i][j_in_list]
                             * (pressures[j] + pressures[i]) / (2 * densities[j])
                             * (Parameters.SMOOTHING_LENGTH - distances[i][j_in_list]) ** 2)

                forces[i] += Parameters.NORMALIZATION_VISCOUS_FORCE \
                             * ((self.velocities[j] - self.velocities[i])
                             / densities[j] * (Parameters.SMOOTHING_LENGTH - distances[i][j_in_list]))

        forces += Parameters.CONSTANT_FORCE

        self.velocities = self.velocities + Parameters.TIME_STEP_LENGTH * forces / densities[:, np.newaxis]
        self.positions = self.positions + Parameters.TIME_STEP_LENGTH * self.velocities

        out_of_left_boundary = self.positions[:, 0] < Parameters.DOMAIN_X_LIM[0]
        out_of_right_boundary = self.positions[:, 0] > Parameters.DOMAIN_X_LIM[1]
        out_of_bottom_boundary = self.positions[:, 1] < Parameters.DOMAIN_Y_LIM[0]
        out_of_top_boundary = self.positions[:, 1] > Parameters.DOMAIN_Y_LIM[1]

        self.velocities[out_of_left_boundary, 0] *= Parameters.DAMPING_COEFFICIENT
        self.positions[out_of_left_boundary, 0] = Parameters.DOMAIN_X_LIM[0]

        self.velocities[out_of_right_boundary, 0] *= Parameters.DAMPING_COEFFICIENT
        self.positions[out_of_right_boundary, 0] = Parameters.DOMAIN_X_LIM[1]

        self.velocities[out_of_bottom_boundary, 1] *= Parameters.DAMPING_COEFFICIENT
        self.positions[out_of_bottom_boundary, 1] = Parameters.DOMAIN_Y_LIM[0]

        self.velocities[out_of_top_boundary, 1] *= Parameters.DAMPING_COEFFICIENT
        self.positions[out_of_top_boundary, 1] = Parameters.DOMAIN_Y_LIM[1]

        counter = 0
        for i in range(len(self.particles)):
            self.particles[i].set_position(self.positions[counter])
            self.particles[i].set_velocity(self.velocities[counter])

            counter += 1

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
        for bound in self.bounds:
            pygame.draw.line(screen, (255, 0, 0), bound[0], bound[1], 3)
