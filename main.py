# MADE BY THIAGO M NÓBREGA
import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()
width, height = 1300, 700
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Define the wave function and calculate the probability density
def wave_function_3d(x, y, z, t):
    sigma = 1.0
    k = 1.0  # wave number
    return np.exp(-(x**2 + y**2 + z**2) / (2 * sigma**2)) * np.exp(-1j * k * (x + y + z))

x, y, z = np.meshgrid(np.linspace(-3, 3, 30), np.linspace(-3, 3, 30), np.linspace(-3, 3, 30))
psi_3d = wave_function_3d(x, y, z, 0)
probability_density = np.abs(psi_3d)**2

# Gravity-like effect based on a massive object
massive_object_pos = np.array([0, 0, 0])  # Position of the massive object
gravitational_constant = 0.1  # Adjust this for stronger/weaker gravity-like effect

# Flatten arrays for easy iteration
particles = np.vstack((x.flatten(), y.flatten(), z.flatten(), probability_density.flatten(), np.zeros_like(x.flatten()), np.zeros_like(y.flatten()), np.zeros_like(z.flatten()))).T

# Camera settings
zoom = 50
angle_x, angle_y = 0, 0

# Function to project 3D point to 2D
def project_3d_to_2d(point, angle_x, angle_y, zoom):
    # Rotation matrices
    cos_y, sin_y = math.cos(math.radians(angle_y)), math.sin(math.radians(angle_y))
    cos_x, sin_x = math.cos(math.radians(angle_x)), math.sin(math.radians(angle_x))

    # Rotation around Y-axis
    x, z = point[0] * cos_y - point[2] * sin_y, point[0] * sin_y + point[2] * cos_y
    y = point[1]

    # Rotation around X-axis
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Perspective projection
    scale = zoom / (5 + z)
    x2d = int(width / 2 + scale * x)
    y2d = int(height / 2 - scale * y)
    return x2d, y2d, scale

def run():
    global angle_x, angle_y, zoom
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Camera control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle_y -= 10
        if keys[pygame.K_RIGHT]:
            angle_y += 10
        if keys[pygame.K_UP]:
            angle_x -= 10
        if keys[pygame.K_DOWN]:
            angle_x += 10
        if keys[pygame.K_a]:
            zoom += 25
        if keys[pygame.K_z]:
            zoom -= 25

        screen.fill((0, 0, 0))

        # Update particles' positions and velocities
        for particle in particles:
            particle_pos = particle[:3]
            direction_to_massive_object = massive_object_pos - particle_pos
            distance_to_massive_object = np.linalg.norm(direction_to_massive_object)
            gravitational_effect = gravitational_constant / distance_to_massive_object**2

            # Adjust velocity towards the massive object
            particle[4:] += gravitational_effect * direction_to_massive_object / distance_to_massive_object

            # Update position based on velocity
            particle[:3] += particle[4:]

        # Draw each particle
        for particle in particles:
            x2d, y2d, scale = project_3d_to_2d(particle, angle_x, angle_y, zoom)
            size = max(1, int(scale * particle[3] * 10))
            color_intensity = int(particle[3] * 255)
            color = (color_intensity, color_intensity, 255)
            pygame.draw.circle(screen, color, (x2d, y2d), size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run()
