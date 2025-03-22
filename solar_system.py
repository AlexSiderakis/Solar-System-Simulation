import sys
import pygame
import math


# general setup
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 600
background = pygame.image.load('space.png')
fps = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

# constants
AU = 149.6e6 * 1000
G = 6.67428e-11
SCALE = 200 / AU  # 1AU = 200 pixels
TIMESTEP = 3600 * 24  # 1 day


class Planet(pygame.sprite.Sprite):
    def __init__(self, image_path, x0, y0, ux0, uy0, mass, name):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.x = x0
        self.y = y0
        self.rect = self.image.get_rect(center=(self.x*SCALE + WIDTH/2, self.y*SCALE + HEIGHT/2))
        self.mass = mass
        self.name = name

        self.vel_x = ux0
        self.vel_y = uy0

    def __str__(self):
        return self.name

    def attraction(self, other):
        distance_x = (other.x - self.x)  # m
        distance_y = (other.y - self.y)  # m
        distance = math.sqrt(distance_x**2 + distance_y**2)

        acceleration = G * other.mass / distance ** 2  # m / s^2
        acc_x = acceleration * distance_x/distance
        acc_y = acceleration * distance_y/distance
        return acc_x, acc_y

    def update(self, group):
        total_acc_x = total_acc_y = 0
        for planet in group:
            if self == planet:
                continue
            if self.x == planet.x and self.y == planet.y:
                continue
            ax, ay = self.attraction(planet)
            total_acc_x += ax
            total_acc_y += ay

        #if self.name == 'sun':
            #total_acc_x = total_acc_y = 0

        self.vel_x += total_acc_x * TIMESTEP  # m/(s x day)
        self.vel_y += total_acc_y * TIMESTEP

        self.x += self.vel_x * TIMESTEP  # m / day
        self.y += self.vel_y * TIMESTEP

        self.rect.centerx = self.x * SCALE + WIDTH / 2
        self.rect.centery = self.y * SCALE + HEIGHT / 2


def main():
    sun = Planet('sun.png', 0, 0, 0, 0, 1.98892 * 10 ** 30, 'sun')
    earth = Planet('earth32.png', -1 * AU, 0, 0, 29.783 * 1000, 5.9742 * 10 ** 24, 'earth')
    venus = Planet('venus32.png', 0.723 * AU, 0, 0, -35.02 * 1000, 4.8685 * 10 ** 24, 'venus')
    mars = Planet('mars24.png', -1.524 * AU, 0, 0, 24.077 * 1000, 6.39 * 10 ** 23, 'mars')
    mercury = Planet('mercury16.png', 0.387 * AU, 0, 0, -47.4 * 1000, 3.30 * 10 ** 23, 'mercury')
    neptune = Planet('neptune64.png', 30.104 * AU, 0, 0, -5.43 * 1000, 1.0241 * 10**26, 'neptune')
    group = pygame.sprite.Group()
    group.add(sun, earth, venus, mars, mercury, neptune)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 50))
        #screen.blit(background, (0, 0))
        group.update(group)
        group.draw(screen)
        pygame.display.update()
        clock.tick(fps)


main()
