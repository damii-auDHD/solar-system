import math
import pygame
from planets import Body

# Visual gravitational constant — tuned so orbital speeds look natural
# on screen.  This is *not* real-world G; it just controls how fast
# planets orbit at a given distance and parent mass.
G_VISUAL = 100

# Golden angle (~137.5°) used to stagger starting positions so planets
# don't all begin in a straight line.
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))

# ── Solar system definition ───────────────────────────────────────
# Every satellite lists its orbital distance from its *parent*.
# Orbital speed is derived automatically via Kepler:  ω = √(G·M/r³)
SOLAR_SYSTEM_DATA = {
    "name": "Sun",
    "radius": 35,
    "mass": 2000,
    "colour": "#FDB813",
    "satellites": [
        {
            "name": "Mercury",
            "radius": 4,
            "mass": 0.1,
            "colour": "#B5B5B5",
            "dist": 65,
        },
        {
            "name": "Venus",
            "radius": 7,
            "mass": 0.8,
            "colour": "#E8CDA0",
            "dist": 105,
        },
        {
            "name": "Earth",
            "radius": 9,
            "mass": 10,
            "colour": "#4B8BBE",
            "dist": 165,
            "satellites": [
                {
                    "name": "Moon",
                    "radius": 3,
                    "mass": 0.05,
                    "colour": "#C0C0C0",
                    "dist": 22,
                }
            ],
        },
        {
            "name": "Mars",
            "radius": 5,
            "mass": 0.3,
            "colour": "#E27B58",
            "dist": 235,
        },
        {
            "name": "Jupiter",
            "radius": 18,
            "mass": 50,
            "colour": "#C88B3A",
            "dist": 340,
            "satellites": [
                {
                    "name": "Io",
                    "radius": 2,
                    "mass": 0.02,
                    "colour": "#F5DEB3",
                    "dist": 28,
                },
                {
                    "name": "Europa",
                    "radius": 2,
                    "mass": 0.02,
                    "colour": "#A8C4D4",
                    "dist": 36,
                },
            ],
        },
        {
            "name": "Saturn",
            "radius": 14,
            "mass": 30,
            "colour": "#E8D191",
            "dist": 440,
            "has_ring": True,
        },
    ],
}


def generate_celestial_tree(node, center_pos,
                            parent_body=None, bodies_list=None,
                            sibling_index=0):
    """Recursively build the solar system tree.

    Each body's orbital speed is derived from Kepler's third law:
        ω = √(G_VISUAL · M_parent / r³)

    Starting angles are staggered by the golden angle so planets
    don't begin in a straight line.
    """
    if bodies_list is None:
        bodies_list = []

    dist = node.get("dist", 0)

    if parent_body is None:
        # ── Root body (the Sun) ───────────────────────────────────
        body = Body(node["name"], node["radius"], node["mass"],
                    node["colour"])
        body.position = pygame.Vector2(center_pos)
    else:
        # ── Satellite — derive orbital speed from Kepler ──────────
        omega = math.sqrt(G_VISUAL * parent_body.mass / (dist ** 3))
        body = Body(node["name"], node["radius"], node["mass"],
                    node["colour"],
                    orbital_distance=dist,
                    orbital_speed=omega,
                    parent=parent_body)

        # Stagger starting angle
        body.orbital_angle = sibling_index * GOLDEN_ANGLE
        body.position = pygame.Vector2(
            parent_body.position.x + math.cos(body.orbital_angle) * dist,
            parent_body.position.y + math.sin(body.orbital_angle) * dist,
        )
        parent_body.satellites.append(body)

    body.has_ring = node.get("has_ring", False)
    bodies_list.append(body)

    # Recurse into satellites
    if "satellites" in node:
        for i, sat_data in enumerate(node["satellites"]):
            generate_celestial_tree(sat_data, center_pos, body,
                                    bodies_list, sibling_index=i)

    return bodies_list


if __name__ == "__main__":
    pygame.init()
    test = generate_celestial_tree(SOLAR_SYSTEM_DATA, pygame.Vector2(640, 450))
    print(f"Success! Built {len(test)} bodies:")
    for b in test:
        parent_name = b.parent.name if b.parent else "—"
        print(f"  {b.name:10s}  parent={parent_name:10s}  "
              f"dist={b.orbital_distance:6.0f}  "
              f"ω={b.orbital_speed:.4f} rad/s")