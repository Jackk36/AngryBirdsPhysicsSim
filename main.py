import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Set up the space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity

# Create the ground as a static rectangle
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Static body
ground_body.position = (300, 370)  # Center of the screen horizontally, near the bottom

# Create the rectangular shape for the ground
ground_shape = pymunk.Poly.create_box(ground_body, (600, 70))  # Width: 600, Height: 70
ground_shape.friction = 0.5
space.add(ground_body, ground_shape)


# Function to draw the floor with a custom color
def draw_floor(screen, ground_shape):
    floor_color = (20, 200, 20)  # Custom color (green in this case)
    vertices = ground_shape.get_vertices()  # Get the vertices of the ground
    points = [(v.x + ground_body.position.x, v.y + ground_body.position.y) for v in vertices]
    pygame.draw.polygon(screen, floor_color, points)  # Draw the floor polygon


# Function to draw pointy grass
def draw_grass(screen, y, ground_shape, color):
    ground_top = 370  # Fixed y-coordinate for the top of the ground
    # Loop to draw grass blades across the top of the ground
    for n in range(4):
        for x in range(-10, 600, 20):  # Grass blades across the ground at intervals
            grass_blade = [(x, y + ground_top - (5 + 4 * n)), (x + 10, y + ground_top - 4 * n),
                           (x + 20, y + ground_top - 5 * (5 + 4 * n))]
            pygame.draw.polygon(screen, color, grass_blade)
        for x in range(20, 600, 20):  # Grass blades across the ground at intervals
            grass_blade = [(x, y + ground_top - (5 + 3 * n)), (x + 10, y + ground_top - 3 * n),
                           (x + 20, y + ground_top - 5 * (5 + 3 * n))]
            pygame.draw.polygon(screen, color, grass_blade)


# Function to create the bird
def create_bird(x, y):
    mass = 1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    bird_body = pymunk.Body(mass, inertia)
    bird_body.position = (x, y)
    bird_shape = pymunk.Circle(bird_body, radius)
    bird_shape.elasticity = 0.8
    space.add(bird_body, bird_shape)
    return bird_body


# Function to draw the sun with a smile and rays
def draw_sun(screen):
    sun_color = (255, 223, 0)  # Yellow
    sun_center = (500, 100)  # Position of the sun
    sun_radius = 50  # Size of the sun

    # Draw rays around the sun
    ray_color = (255, 200, 0)  # Lighter yellow for rays
    for angle in range(0, 360, 30):  # Rays at 30-degree intervals
        x_end = sun_center[0] + sun_radius * 1.5 * math.cos(math.radians(angle))
        y_end = sun_center[1] + sun_radius * 1.5 * math.sin(math.radians(angle))
        pygame.draw.line(screen, ray_color, sun_center, (x_end, y_end), 3)

    # Draw the sun (circle)
    pygame.draw.circle(screen, sun_color, sun_center, sun_radius)

    # Draw the eyes (two small circles)
    eye_color = (0, 0, 0)  # Black
    pygame.draw.circle(screen, eye_color, (480, 85), 7)  # Left eye
    pygame.draw.circle(screen, eye_color, (520, 85), 7)  # Right eye

    # Draw the smiling mouth (arc)
    mouth_color = (0, 0, 0)  # Black
    pygame.draw.arc(screen, mouth_color, [470, 90, 60, 40], 3.14, 0, 3)  # Draw the smile (arc)


# Function to draw the wooden slingshot with more detail
def draw_slingshot(screen):
    slingshot_color = (139, 69, 19)  # Brown color for the wood
    shadow_color = (115, 55, 17)  # Darker brown for shading

    # Base of the slingshot (rounded bottom)
    pygame.draw.rect(screen, slingshot_color, (80, 300, 40, 80))  # Rounded base
    pygame.draw.rect(screen, shadow_color, (85, 335, 30, 40))  # Shading for rounded base

    # Thicker arms of the slingshot forming a "V" shape
    pygame.draw.polygon(screen, slingshot_color, [(80, 330), (70, 290), (65, 250), (85, 250), (90, 290)])  # Left arm
    pygame.draw.polygon(screen, slingshot_color,
                        [(120, 330), (130, 290), (145, 250), (115, 250), (110, 290)])  # Right arm

    # Rubber band between the arms
    band_color = (150, 75, 0)  # Slightly darker for the rubber band
    pygame.draw.line(screen, band_color, (85, 150), (115, 150), 5)  # Band connecting the two arms at the top

    # Add wood grain effect (lines for details)
    pygame.draw.line(screen, shadow_color, (95, 330), (95, 380), 2)  # Grain on the left side of the base
    pygame.draw.line(screen, shadow_color, (105, 330), (105, 380), 2)  # Grain on the right side of the base


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((200, 220, 255))  # Blue background (sky)

    # Update physics
    space.step(1 / 50.0)  # Simulate physics with a fixed time step

    # Draw the smiling sun in the background with rays
    draw_sun(screen)

    # Draw the custom floor
    draw_floor(screen, ground_shape)



    # Draw the grass on top of the ground
    draw_grass(screen, 40, ground_shape, (34, 139, 34))
    draw_grass(screen, 22, ground_shape, (4, 109, 4))
    draw_grass(screen, 0, ground_shape, (34, 139, 34))

    # Draw the wooden slingshot with enhanced details
    draw_slingshot(screen)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
