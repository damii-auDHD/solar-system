import pygame
import math
from planets import Body

G = 20000

def calculate_stable_orbit(sun: Body, earth: Body, tracking_radius=300.0):
    if sun.mass < 1000.0:
        orbit_radius = tracking_radius + 150.0  
    else:
        orbit_radius = tracking_radius  

    earth.position = pygame.Vector2(sun.position.x, sun.position.y - orbit_radius)
    orbital_speed = math.sqrt((G * sun.mass) / orbit_radius)
    earth.velocity = pygame.Vector2(orbital_speed, 0)
    
    return orbit_radius

def apply_universal_gravity(bodies: list):
    for body in bodies:
        body.acceleration = pygame.Vector2(0, 0)

    for i, body_a in enumerate(bodies):
        for j, body_b in enumerate(bodies):
            if i == j:
                continue
                
            direction_vector = body_b.position - body_a.position
            distance = direction_vector.length()
            
            if distance < 1.0: 
                continue

            direction_normalized = direction_vector.normalize()
            acceleration_magnitude = (G * body_b.mass) / (distance ** 2)
            body_a.acceleration += direction_normalized * acceleration_magnitude


if __name__ == "__main__":
    pygame.init()
    all_test_bodies = [
        Body("Sun", 40, 2000, "orange", (640, 500), (0, 0)),
        Body("Earth", 12, 1, "blue", (640, 200), (200, 0))
    ]
    apply_universal_gravity(all_test_bodies)
    print(f"Success! Computed Earth Acceleration Vector: {all_test_bodies[1].acceleration}")