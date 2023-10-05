import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass, name, texture, semi_major_axis, eccentricity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name  # Name of the planet
        self.texture = pygame.image.load(texture)
        self.texture = pygame.transform.scale(self.texture, (2 * self.radius, 2 * self.radius))

        self.orbit = []  # Stores points of the planet's orbit
        self.sun = False  # Indicates if it's the Sun
        self.distance_to_sun = 0  # Distance from the Sun

        # Orbital parameters for elliptical orbits
        self.semi_major_axis = semi_major_axis  # Semi-major axis of the elliptical orbit
        self.eccentricity = eccentricity  # Eccentricity of the orbit
        self.angle = math.atan2(y, x)  # Initial angle for elliptical orbit
        self.initial_distance = math.sqrt(x**2 + y**2)  # Initial distance from the Sun

        # Initialize initial_x and initial_y
        self.initial_x = self.x
        self.initial_y = self.y

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = int(self.x * self.SCALE + WIDTH / 2)
        y = int(self.y * self.SCALE + HEIGHT / 2)

        # Draw planet texture instead of a simple circle
        win.blit(self.texture, (x - self.radius, y - self.radius))

        # Display the planet's name above the planet
        planet_name = FONT.render(self.name, 1, WHITE)
        win.blit(planet_name, (x - planet_name.get_width() / 2, y + self.radius + 5))  # Adjust the position

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = int(x * self.SCALE + WIDTH / 2)
                y = int(y * self.SCALE + HEIGHT / 2)
                updated_points.append((x, y))

            # Draw the orbit path
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            # Display the distance from the Sun
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        # Calculate gravitational force
        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Calculate the current angle for the elliptical orbit
        self.angle += math.radians(0.1)  # Adjust the angular velocity as needed
        # Calculate the current distance from the Sun based on the elliptical orbit
        current_distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 + self.eccentricity * math.cos(self.angle))
        # Calculate the current position based on the angle and distance
        self.x = current_distance * math.cos(self.angle)
        self.y = current_distance * math.sin(self.angle)
        # Calculate the current velocity based on the change in position
        self.x_vel = (self.x - self.initial_x) / self.TIMESTEP
        self.y_vel = (self.y - self.initial_y) / self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    # Update planet objects with realistic parameters
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun", "sun.png", 0, 0)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, "Earth", "earth.png", Planet.AU, 0.0167)
    # Set the eccentricity and semi-major axis based on Earth's orbit

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "Mars", "mars.png", 1.524 * Planet.AU, 0.0934)
    # Set the eccentricity and semi-major axis based on Mars's orbit

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, "Mercury", "mercury.png", 0.387 * Planet.AU, 0.2056)
    # Set the eccentricity and semi-major axis based on Mercury's orbit

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "Venus", "venus.png", 0.723 * Planet.AU, 0.0067)
    # Set the eccentricity and semi-major axis based on Venus's orbit

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
