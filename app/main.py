import pygame
from planets import Body
import physics
import solar_system

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("monospace", 12, bold=True)

size = width, height = 1280, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Recursive N-Body Gravity Engine")

clock = pygame.time.Clock()
dt = 0

center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

all_celestial_bodies = []
solar_system.generate_celestial_tree(solar_system.SOLAR_SYSTEM_DATA, center, 0, all_celestial_bodies)

sun_reference = all_celestial_bodies[0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sun_reference.change_mass(sun_reference.mass + 500)
            elif event.key == pygame.K_DOWN:
                sun_reference.change_mass(sun_reference.mass - 500)

    physics.apply_universal_gravity(all_celestial_bodies)
    
    # Split the frame time into 4 ultra-precise mini steps
    sub_steps = 4
    mini_dt = dt / sub_steps
    
    for _ in range(sub_steps):
        physics.apply_universal_gravity(all_celestial_bodies) # Re-calculate forces for accuracy
        for body in all_celestial_bodies:
            if body == sun_reference:
                continue
            body.velocity += body.acceleration * mini_dt
            body.position += body.velocity * mini_dt

    screen.fill('black') 
    
    for radius_guide in [80, 130, 210, 290, 390]:
        pygame.draw.circle(screen, (35, 35, 35), center, radius_guide, width=1)
    
    for body in all_celestial_bodies:
        body.draw(screen, my_font, track_target=sun_reference)

    pygame.display.flip()
    dt = clock.tick(60) / 1000.0

pygame.quit()