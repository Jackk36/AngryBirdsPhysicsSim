import pygame
import pymunk
import pymunk.pygame_util

# Initialize Pygame and Pymunk
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Angry Birds in Python")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)

# Draw options
draw_options = pymunk.pygame_util.DrawOptions(screen)

slingshot_pos = (100, 590)  # Starting point of the bird (slingshot center)
max_drag_distance = 50     # Max distance allowed for dragging (circle radius)

# Create ground and bird
def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (400, 600)
    shape = pymunk.Segment(body, (-400, 0), (600, 0), 5)
    shape.elasticity = 0.0
    space.add(body, shape)
def create_bird(x, y):
    mass = 1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    bird_body = pymunk.Body(mass, inertia)
    bird_body.position = (x, y)
    bird_shape = pymunk.Circle(bird_body, radius)
    bird_shape.elasticity = 0.8
    bird_shape.friction = 1.0
    space.add(bird_body, bird_shape)
    return bird_body

def blocks(x, y, width, height):
    mass = 0.1
    inertia = pymunk.moment_for_box(mass, (width, height))

    # Create the body
    block_body = pymunk.Body(mass, inertia)
    block_body.position = (x, y)

    # Define the box shape with vertices relative to the center of the block
    half_width = width / 2
    half_height = height / 2
    vertices = [
        (-half_width, -half_height),  # Bottom-left corner
        (half_width, -half_height),  # Bottom-right corner
        (half_width, half_height),  # Top-right corner
        (-half_width, half_height)  # Top-left corner
    ]

    # Create the shape using these relative vertices
    block_shape = pymunk.Poly(block_body, vertices)
    block_shape.elasticity = 0.0
    block_shape.friction = 1.0

    # Add the body and shape to the space
    space.add(block_body, block_shape)

    return block_body


create_ground()
bird = create_bird(*slingshot_pos)
blocks(400,400, 50, 75)
blocks(450,400, 50, 75)
blocks(500,400, 50, 75)

blocks(425,320, 50, 75)
blocks(475,320, 50, 75)

blocks(450,245, 50, 75)

# Main game loop
running = True
dragging = False
launch_power = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if bird.position.get_distance(mouse_pos) < 20:
                dragging = True
                bird.velocity = (0, 0)  # Stop any falling during drag
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                launch_velocity = (bird.position - mouse_pos) * launch_power
                bird.velocity = launch_velocity
                dragging = False
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the vector from the slingshot to the mouse
        drag_vector = pymunk.Vec2d(mouse_x, mouse_y) - slingshot_pos

        # If the distance is greater than the max_drag_distance, restrict it
        if drag_vector.length > max_drag_distance:
            drag_vector = drag_vector.normalized() * max_drag_distance

        # Set the bird's position based on the restricted drag vector
        bird.position = slingshot_pos + drag_vector
        bird.velocity = (0, 0)


    # Update physics
    space.step(1/60)

    # Clear screen and draw everything
    screen.fill((135, 206, 235))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
