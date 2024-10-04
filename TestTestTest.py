import pygame
import pymunk
import pymunk.pygame_util

# Initialize Pygame and Pymunk
pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Angry Birds in Python")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)

# Draw options
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Collision types
BIRD_COLLISION_TYPE = 1
BLOCK_COLLISION_TYPE = 2
GROUND_COLLISION_TYPE = 3

slingshot_pos = (100, 500)  # Starting point of the bird (slingshot center)
max_drag_distance = 50     # Max distance allowed for dragging (circle radius)

# Create ground and bird
def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (400, 600)
    shape = pymunk.Segment(body, (-400, 0), (600, 0), 5)
    shape2 = pymunk.Segment(body, (-400, 0), (-400, -600), 5)
    shape3 = pymunk.Segment(body, (600, -600), (600, 0), 5)

    shape.collision_type = GROUND_COLLISION_TYPE

    shape.elasticity = 0.0
    shape2.elasticity = 1.0
    shape3.elasticity = 1.0
    shape.friction = 1.0

    body.velocity = (0,0)

    space.add(body, shape, shape2, shape3)

def create_bird(x, y):
    mass = 1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    bird_body = pymunk.Body(mass, inertia)
    bird_body.position = (x, y)
    bird_shape = pymunk.Circle(bird_body, radius)
    bird_shape.elasticity = 0.8
    bird_shape.collision_type = BIRD_COLLISION_TYPE  # Set bird collision type
    bird_shape.friction = 1.0
    bird_body.velocity = (0,0)
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
    block_shape.collision_type = BLOCK_COLLISION_TYPE  # Set block collision type
    block_shape.friction = 1.0

    block_body.velocity = (0,0)

    # Add the body and shape to the space
    space.add(block_body, block_shape)

    return block_body

def handle_bird_block_collision(arbiter, space, data):
    """Callback function to handle bird-block collision."""
    block_shape = arbiter.shapes[1]  # The block is the second shape in the collision pair

    # Remove the block's body and shape from the space
    space.remove(block_shape, block_shape.body)

    return True  # Continue with the normal collision processing
def handle_block_ground_collision(arbiter, space, data):
    block_shape = arbiter.shapes[1]
    block_body = block_shape.body

    # Check if the block is falling
    falling_threshold = 200  # A threshold velocity to consider the block as falling
    if block_body.velocity.y > falling_threshold:
        # The block is falling, so remove it from the space
        space.remove(block_shape, block_shape.body)

    return True


def draw_trajectory(surface, bird_body, drag_vector, steps=10, step_size=0.1):
    """Draws the trajectory of the bird using small dots."""
    # Launch power based on drag
    launch_power_scaled = drag_vector.length / max_drag_distance * launch_power
    initial_velocity = -drag_vector.normalized() * launch_power_scaled * 10  # Calculate launch velocity

    bird_pos = pymunk.Vec2d(bird_body.position.x, bird_body.position.y)  # Get current bird position

    for i in range(steps):
        t = step_size * i  # Time step

        # Predict future position using physics equations
        future_pos_x = bird_pos.x + initial_velocity.x * t
        future_pos_y = bird_pos.y + initial_velocity.y * t + 0.5 * space.gravity[1] * t ** 2

        # Convert to screen coordinates (Pygame's inverted Y-axis)
        future_pos_screen = (int(future_pos_x), int(future_pos_y))

        # Draw trajectory dots if within screen bounds
        pygame.draw.circle(surface, (255, 0, 0), future_pos_screen, 5)


create_ground()
bird = create_bird(*slingshot_pos)

blocks(400,550, 50, 75) #leg 1
blocks(500,550, 50, 75) #leg 2

blocks(400, 475, 100, 50) #top part 1
blocks(500, 475, 100, 50) #top part 2

blocks(400,425, 50, 75) #leg 3
blocks(500,425, 50, 75) #leg 4

blocks(400, 350, 100, 50) #top part 3
blocks(500, 350, 100, 50) #top part 4


# Add a collision handler for bird-block collisions
collision_handler = space.add_collision_handler(BIRD_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
collision_handler.begin = handle_bird_block_collision  # Set the callback

block_ground_collision_handler = space.add_collision_handler(GROUND_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_ground_collision_handler.begin = handle_block_ground_collision  # Set the callback


# Main game loop
running = True
dragging = False
launch_power = 100
initial_mouse_pos = None  # Store initial click position
bird_launched = False  # Track whether the bird has been launched

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if bird.position.get_distance(mouse_pos) < 20 and not bird_launched:
                dragging = True
                bird.velocity = (0, 0)  # Stop any falling during drag
                initial_mouse_pos = mouse_pos  # Set initial mouse position when dragging starts
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging and initial_mouse_pos and not bird_launched:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_mouse_pos = pymunk.Vec2d(mouse_x, mouse_y)  # Get the current mouse position
                drag_vector = current_mouse_pos - initial_mouse_pos  # Calculate the drag vector based on initial click position

                # Scale the launch velocity based on the drag distance, clamped to max_drag_distance
                if drag_vector.length > max_drag_distance:
                    drag_vector = drag_vector.normalized() * max_drag_distance * 10

                # Calculate launch velocity and apply it to the bird
                launch_velocity = -drag_vector.normalized() * (drag_vector.length / max_drag_distance * launch_power)
                bird.velocity = launch_velocity
                dragging = False
                bird_launched = True  # Set bird as launched after release
                initial_mouse_pos = None  # Store initial click position

                print(f"Drag Vector: {drag_vector}, Launch Velocity: {launch_velocity}")
                print(f"Bird Position: {bird.position}, Bird Velocity: {bird.velocity}")  # Check the state of the bird

    # Keep the bird floating until launched
    if not bird_launched and not dragging:
        bird.velocity = (0, 0)  # Ensure bird stays in place until launched
        bird.position = slingshot_pos  # Reset bird position to the slingshot


    # Update physics
    space.step(1/60)


    # Clear screen and draw everything
    screen.fill((135, 206, 235))
    space.debug_draw(draw_options)
    # Update the bird's position while dragging
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        current_mouse_pos = pymunk.Vec2d(mouse_x, mouse_y)  # Get current mouse position
        drag_vector = current_mouse_pos - initial_mouse_pos  # Calculate drag vector based on the initial click

        # Ensure we do not exceed max drag distance
        if drag_vector.length > max_drag_distance:
            drag_vector = drag_vector.normalized() * max_drag_distance

        # Set bird's position to slingshot position + drag vector
        bird.position = slingshot_pos + drag_vector  # Update bird's position based on the drag
        bird.velocity = (0, 0)  # Bird doesn't move while dragging

        # Draw the predicted trajectory while dragging
        draw_trajectory(screen, bird, drag_vector)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
