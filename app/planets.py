import pygame

class Body:
    def __init__(self, name: str, radius: float, mass: float, colour: str, position: tuple, velocity: tuple):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.colour = colour
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2(0, 0)

    def change_mass(self, new_mass: float):
        self.mass = new_mass
        self.radius = max(4.0, (self.mass) ** 0.33 * 4) 

    def draw(self, screen, font, track_target=None):
        pygame.draw.circle(screen, self.colour, self.position, int(self.radius))
        
        text_surface = font.render(self.name, True, "white")
        text_position = (self.position.x - (text_surface.get_width() / 2), 
                         self.position.y - self.radius - 20)
        screen.blit(text_surface, text_position)
        
        if track_target and track_target != self:
            distance = self.position.distance_to(track_target.position)
            dist_surface = font.render(f"{int(distance)}px", True, "gray")
            dist_position = (self.position.x - (dist_surface.get_width() / 2), 
                             self.position.y - self.radius - 5)
            screen.blit(dist_surface, dist_position)

    def __repr__(self):
        return f'=== Celestial body info ===\nName: {self.name}\nColour: {self.colour}\nMass: {self.mass}\nRadius: {self.radius}\n==========================='