import pygame
import math
from collections import deque


class Body:
    """A celestial body that orbits a parent using parametric Kepler motion."""

    def __init__(self, name, radius, mass, colour,
                 orbital_distance=0, orbital_speed=0, parent=None):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.colour = colour
        self.parent = parent
        self.orbital_distance = orbital_distance
        self.orbital_speed = orbital_speed      # radians / second
        self.orbital_angle = 0.0                # current angle (set by generator)
        self.position = pygame.Vector2(0, 0)
        self.satellites = []
        self.has_ring = False

        # Fading orbit trail
        self.trail = deque(maxlen=400)
        self._trail_tick = 0

    # ── update ────────────────────────────────────────────────────
    def update(self, dt):
        """Advance the orbital angle and recompute position relative to parent."""
        if self.parent is None:
            return                              # root body stays put

        self.orbital_angle += self.orbital_speed * dt

        self.position.x = (self.parent.position.x
                           + math.cos(self.orbital_angle) * self.orbital_distance)
        self.position.y = (self.parent.position.y
                           + math.sin(self.orbital_angle) * self.orbital_distance)

        # record trail point every few ticks
        self._trail_tick += 1
        if self._trail_tick % 3 == 0:
            self.trail.append(pygame.Vector2(self.position))

    # ── drawing helpers ───────────────────────────────────────────
    def draw_orbit_path(self, screen):
        """Draw the faint circular orbit guide around the parent."""
        if self.parent:
            pygame.draw.circle(
                screen, (25, 25, 50),
                (int(self.parent.position.x), int(self.parent.position.y)),
                int(self.orbital_distance), width=1,
            )

    def draw_trail(self, screen):
        """Draw a trail that fades from dark to the body's colour."""
        if len(self.trail) < 2:
            return
        points = list(self.trail)
        base = pygame.Color(self.colour)
        for i in range(1, len(points)):
            t = i / len(points)
            colour = (
                max(0, min(255, int(base.r * t * 0.5))),
                max(0, min(255, int(base.g * t * 0.5))),
                max(0, min(255, int(base.b * t * 0.5))),
            )
            pygame.draw.line(screen, colour, points[i - 1], points[i], 1)

    def draw(self, screen, font):
        """Draw the body circle, optional ring, and name label."""
        px, py = int(self.position.x), int(self.position.y)

        # Saturn-style ring
        if self.has_ring:
            ring_rect = pygame.Rect(0, 0,
                                    int(self.radius * 3.5),
                                    int(self.radius * 1.2))
            ring_rect.center = (px, py)
            pygame.draw.ellipse(screen, "#C8AD7F", ring_rect, 2)

        # Body disc
        pygame.draw.circle(screen, self.colour, (px, py), int(self.radius))

        # Name label
        label = font.render(self.name, True, "white")
        screen.blit(label,
                     (px - label.get_width() // 2,
                      py - int(self.radius) - 16))

    # ── repr ──────────────────────────────────────────────────────
    def __repr__(self):
        return (f"Body('{self.name}', r={self.radius}, m={self.mass}, "
                f"dist={self.orbital_distance})")