import pygame
import pymunk
import pymunk.pygame_util

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
ground_body.position = (300, 350)  # Center of the screen horizontally, near the bottom

# Create the rectangular shape for the ground
ground_shape = pymunk.Poly.create_box(ground_body, (500, 50))  # Width: 500, Height: 50
ground_shape.friction = 0.5
space.add(ground_body, ground_shape)


# Create a dynamic "bird" (circle) that is summoned on mouse click
def summon_bird(position):
    bird_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))  # Mass: 1, Radius: 15
    bird_body.position = position
    bird_shape = pymunk.Circle(bird_body, 15)  # Radius of the circle (bird)
    bird_shape.friction = 0.5
    bird_shape.elasticity = 0.8  # Add some bounce to the bird
    bird_shape.color = pygame.Color("yellow")  # Optional: Set the color of the bird
    space.add(bird_body, bird_shape)
    return bird_body, bird_shape


# List to hold summoned birds
birds = []


# Function to draw the floor with a custom color
def draw_floor(screen, ground_shape):
    floor_color = (0, 128, 255)  # Custom color (blue in this case)
    vertices = ground_shape.get_vertices()  # Get the vertices of the ground
    points = [(v.x + ground_body.position.x, v.y + ground_body.position.y) for v in vertices]
    pygame.draw.polygon(screen, floor_color, points)  # Draw the floor polygon


# Function to draw pointy grass
def draw_grass(screen, ground_shape):
    ground_rect = ground_shape.get_vertices()  # Get the vertices of the ground
    ground_top = min([v.y for v in ground_rect])  # Get the top y-coordinate of the ground
    grass_color = (34, 139, 34)  # A nice green color for the grass

    # Loop to draw grass blades across the top of the ground
    for x in range(100, 500, 20):  # Grass blades across the ground at intervals
        # Points of the grass triangle
        grass_blade = [(x, ground_top - 5), (x + 10, ground_top - 20), (x + 20, ground_top - 5)]
        pygame.draw.polygon(screen, grass_color, grass_blade)


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Summon the bird on mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            mouse_position = pygame.mouse.get_pos()
            # Convert Pygame coordinates to Pymunk (inverted Y axis)
            bird = summon_bird(mouse_position)
            birds.append(bird)

    screen.fill((255, 255, 255))  # White background

    # Update physics
    space.step(1 / 50.0)  # Simulate physics with a fixed time step

    # Draw the custom floor
    draw_floor(screen, ground_shape)

    # Draw the grass on top of the ground
    draw_grass(screen, ground_shape)

    # Draw the birds (circles) that have been summoned
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
