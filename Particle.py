import pygame
import numpy as np
import Parameters


class Particle:
    def __init__(self):
        self.position = np.array([[10 + np.random.rand(), 250]])
        self.velocity = np.array([[np.random.randint(-10, 10), np.random.randint(-10, 10)]])

    def set_position(self, new_position):
        self.position = new_position

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def draw(self, screen):
        #print(self.position)
        pygame.draw.circle(screen, (0, 0, 255), (self.position[0], self.position[1]), Parameters.SCATTER_DOT_SIZE)
        pygame.draw.line(screen, (255, 0, 0), (self.position[0], self.position[1]), (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]), 1)
