import math
import pygame
from planets import Body

SOLAR_SYSTEM_DATA = {
    "name": "Sun", "radius": 40.0, "mass": 2000.0, "colour": "orange", "dist": 0, "speed_mult": 1.0,
    "satellites": [
        {"name": "Mercury", "radius": 4.0, "mass": 0.1, "colour": "darkgray", "dist": 80, "speed_mult": 1.0},
        {"name": "Venus", "radius": 7.0, "mass": 0.8, "colour": "gold", "dist": 130, "speed_mult": 1.0},
        {
            "name": "Earth", "radius": 10.0, "mass": 10.0, "colour": "blue", "dist": 210, "speed_mult": 1.0, # Beefed up Earth's mass to 10.0 to hold its Moon!
            "satellites": [
                {"name": "Moon", "radius": 3.0, "mass": 0.05, "colour": "lightgray", "dist": 25, "speed_mult": 1.0} # Lowered speed multiplier to 1.0
            ]
        },
        {"name": "Mars", "radius": 6.0, "mass": 0.15, "colour": "red", "dist": 300, "speed_mult": 0.95}, # Lowered speed multiplier to 0.95 so it stays tracked
        {"name": "Jupiter", "radius": 20.0, "mass": 20.0, "colour": "peru", "dist": 400, "speed_mult": 1.0}
    ]
}
G = 20000

def generate_celestial_tree(node: dict, center_pos: pygame.Vector2, parent_mass: float, bodies_list: list, parent_vel=pygame.Vector2(0,0)):
    if node["dist"] == 0:
        spawn_pos = pygame.Vector2(center_pos)
        initial_vel = pygame.Vector2(0, 0)
    else:
        spawn_pos = pygame.Vector2(center_pos.x, center_pos.y - node["dist"])
        orbital_speed = math.sqrt((G * parent_mass) / node["dist"]) * node["speed_mult"]
        initial_vel = pygame.Vector2(orbital_speed, 0) + parent_vel

    new_body = Body(node["name"], node["radius"], node["mass"], node["colour"], spawn_pos, initial_vel)
    bodies_list.append(new_body)

    if "satellites" in node:
        for satellite in node["satellites"]:
            generate_celestial_tree(satellite, new_body.position, new_body.mass, bodies_list, new_body.velocity)


if __name__ == "__main__":
    pygame.init()
    test_arr = []
    generate_celestial_tree(SOLAR_SYSTEM_DATA, pygame.Vector2(640, 500), 0, test_arr)
    print(f"Success! Recursive system mapped out. Total Objects: {len(test_arr)}")