import pygame
import random
import solar_system

# ── Initialisation ────────────────────────────────────────────────
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

font = pygame.font.SysFont("monospace", 11, bold=True)
hud_font = pygame.font.SysFont("monospace", 13, bold=True)
clock = pygame.time.Clock()

center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

# ── Build the solar system ────────────────────────────────────────
all_bodies = solar_system.generate_celestial_tree(
    solar_system.SOLAR_SYSTEM_DATA, center
)
sun = all_bodies[0]

# ── Background stars (deterministic) ─────────────────────────────
random.seed(42)
stars = []
for _ in range(250):
    sx = random.randint(0, WIDTH)
    sy = random.randint(0, HEIGHT)
    brightness = random.randint(60, 180)
    size = random.choices([1, 2], weights=[85, 15])[0]
    stars.append((sx, sy, brightness, size))

# ── Pre-render sun glow ──────────────────────────────────────────
GLOW_RADIUS = 90
glow_surface = pygame.Surface((GLOW_RADIUS * 2, GLOW_RADIUS * 2),
                               pygame.SRCALPHA)
for r in range(GLOW_RADIUS, 0, -1):
    alpha = int(25 * (r / GLOW_RADIUS))
    pygame.draw.circle(glow_surface, (255, 200, 50, alpha),
                       (GLOW_RADIUS, GLOW_RADIUS), r)

# ── Main loop ─────────────────────────────────────────────────────
speed_mult = 1.0
paused = False
running = True

while running:
    raw_dt = clock.tick(60) / 1000.0
    dt = 0.0 if paused else raw_dt * speed_mult

    # ── events ────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                speed_mult = min(5.0, round(speed_mult + 0.25, 2))
            elif event.key == pygame.K_DOWN:
                speed_mult = max(0.25, round(speed_mult - 0.25, 2))
            elif event.key == pygame.K_SPACE:
                paused = not paused

    # ── update (parents always come before children in the list) ──
    for body in all_bodies:
        body.update(dt)

    # ── draw ──────────────────────────────────────────────────────
    screen.fill((5, 5, 15))

    # background stars
    for sx, sy, sb, ss in stars:
        pygame.draw.circle(screen, (sb, sb, min(255, sb + 20)),
                           (sx, sy), ss)

    # orbit guide circles
    for body in all_bodies:
        body.draw_orbit_path(screen)

    # fading trails
    for body in all_bodies:
        body.draw_trail(screen)

    # sun glow (drawn before the sun disc)
    screen.blit(glow_surface,
                (int(sun.position.x) - GLOW_RADIUS,
                 int(sun.position.y) - GLOW_RADIUS))

    # celestial bodies
    for body in all_bodies:
        body.draw(screen, font)

    # HUD
    state = "PAUSED" if paused else f"{speed_mult:.2f}x"
    hud_text = hud_font.render(
        f"Speed: {state}  |  \u2191\u2193 speed  |  SPACE pause",
        True, (80, 80, 100),
    )
    screen.blit(hud_text, (10, HEIGHT - 28))

    pygame.display.flip()

pygame.quit()