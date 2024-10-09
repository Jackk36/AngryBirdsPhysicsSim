import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# image loading stuff
bird_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/BirdImage.png")  # Path to your uploaded image
bird_rect = bird_image.get_rect()

hit_bird_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/BirdHit.png")

medium_block = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/"
                                 "MedBlock.png")
medium_block = pygame.transform.scale(medium_block, (100,50))
medium_block_hit_1 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/"
                                 "MedBlockHit1.png")
medium_block_hit_2 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/"
                                 "MedBlockHit2.png")
medium_block_hit_3 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/"
                                 "MedBlockHit3.png")

# Set up the space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity

# Collision types
BIRD_COLLISION_TYPE = 1
BLOCK_COLLISION_TYPE = 2
GROUND_COLLISION_TYPE = 3

slingshot_pos = (100, 600)  # Starting point of the bird (slingshot center)
max_drag_distance = 100     # Max distance allowed for dragging (circle radius)

# Create the ground as a static rectangle
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Static body
ground_body.position = (600, 780)  # Center of the screen horizontally, near the bottom

# Create the rectangular shape for the ground
ground_shape = pymunk.Poly.create_box(ground_body, (2200, 70))  # Width: 600, Height: 70
ground_shape.friction = 0.5
ground_shape.collision_type = GROUND_COLLISION_TYPE
space.add(ground_body, ground_shape)

def draw_floor(screen, ground_shape):
    floor_color = (20, 200, 20)  # Custom color (green in this case)
    vertices = ground_shape.get_vertices()  # Get the vertices of the ground
    points = [(v.x + ground_body.position.x, v.y + ground_body.position.y) for v in vertices]
    pygame.draw.polygon(screen, floor_color, points)  # Draw the floor polygon
def draw_grass(screen, y, ground_shape, color):
    ground_top = 790  # Fixed y-coordinate for the top of the ground
    # Loop to draw grass blades across the top of the ground
    for n in range(4):
        for x in range(-10, 1200, 20):  # Grass blades across the ground at intervals
            grass_blade = [(x, y + ground_top - (5 + 4 * n)), (x + 10, y + ground_top - 4 * n),
                           (x + 20, y + ground_top - 5 * (5 + 4 * n))]
            pygame.draw.polygon(screen, color, grass_blade)
        for x in range(20, 1200, 20):  # Grass blades across the ground at intervals
            grass_blade = [(x, y + ground_top - (5 + 3 * n)), (x + 10, y + ground_top - 3 * n),
                           (x + 20, y + ground_top - 5 * (5 + 3 * n))]
            pygame.draw.polygon(screen, color, grass_blade)
def draw_bird(screen, bird_body):
    bird_position = bird_body.position
    bird_angle_degrees = math.degrees(bird_body.angle)  # Convert angle to degrees for Pygame

    # Rotate the bird image based on the bird's angle
    rotated_bird_image = pygame.transform.rotate(bird_image,
                                                 -bird_angle_degrees)  # Rotate image (negative for correct direction)

    # Update the rectangle to keep the image centered on the bird's position
    rotated_rect = rotated_bird_image.get_rect(center=(bird_position.x-5, bird_position.y))

    # Blit the rotated image at the updated position
    screen.blit(rotated_bird_image, rotated_rect.topleft)
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
def draw_sun(screen):
    sun_color = (255, 223, 0)  # Yellow
    sun_center = (1100, 100)  # Position of the sun
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
    pygame.draw.circle(screen, eye_color, (1060, 70), 7)  # Left eye
    pygame.draw.circle(screen, eye_color, (1140, 70), 7)  # Right eye

    # Draw the smiling mouth (arc)
    mouth_color = (0, 0, 0)  # Black
    pygame.draw.arc(screen, mouth_color, [1080, 80, 60, 40], 3.14, 0, 3)  # Draw the smile (arc)
def draw_slingshot(screen):
    slingshot_color = (139, 69, 19)  # Brown color for the wood
    shadow_color = (115, 55, 17)  # Darker brown for shading

    # Base of the slingshot (rounded bottom)
    pygame.draw.rect(screen, slingshot_color, (80, 690, 40, 100))  # Rounded base
    pygame.draw.rect(screen, shadow_color, (85, 740, 30, 40))  # Shading for rounded base

    # Thicker arms of the slingshot forming a "V" shape
    pygame.draw.polygon(screen, slingshot_color, [(80, 770), (50, 690), (35, 610), (65, 610), (80, 690)])  # Left arm
    pygame.draw.polygon(screen, slingshot_color,
                        [(120, 770), (150, 690), (165, 610), (135, 610), (120, 690)])  # Right arm

    # Add wood grain effect (lines for details)
    pygame.draw.line(screen, shadow_color, (95, 720), (95, 750), 2)  # Grain on the left side of the base
    pygame.draw.line(screen, shadow_color, (105, 720), (105, 750), 2)  # Grain on the right side of the base
def blocks(x, y, width, height, is_intact, created):
    mass = 1.0
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

    block_body.width = width
    block_body.height = height

    block_body.is_intact = is_intact
    block_body.created = created
    block_body.shape = block_shape

    # Add the body and shape to the space
    if created:
        space.add(block_body, block_shape)

    return block_body
def draw_blocks(screen, block_body):
    if block_body.is_intact:
        block_position = block_body.position
        block_angle_degrees = math.degrees(block_body.angle)

        # Determine whether to draw the block normally or rotated
        if block_body.width > block_body.height:
            # Draw normally
            rotated_block_image = pygame.transform.rotate(medium_block, -block_angle_degrees)
        else:
            # Draw rotated 90 degrees
            rotated_block_image = pygame.transform.rotate(medium_block, -block_angle_degrees + 90)

        rotated_rect = rotated_block_image.get_rect(center=(block_position.x, block_position.y))

        screen.blit(rotated_block_image, rotated_rect.topleft)
def handle_bird_block_collision(arbiter, space, data):
    """Callback function to handle bird-block collision."""
    block_shape = arbiter.shapes[1]  # The block is the second shape in the collision pair

    velocity_threshold = 200  # A threshold velocity to consider the block as falling

    # Remove the block's body and shape from the space
    if bird.velocity.y > velocity_threshold:
        space.remove(block_shape, block_shape.body)
        block_shape.body.is_intact = False

    # Collision handler to detect bird hitting block
    def bird_hit_block(arbiter, space, data):
        global bird_image  # Modify global bird_image when the collision occurs
        bird_image = hit_bird_image  # Change bird's image to the new one
        return True  # Return True to process the collision

    # Add the collision handler
    handler = space.add_collision_handler(BIRD_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
    handler.post_solve = bird_hit_block  # Call bird_hit_block function when collision occurs

    return True  # Continue with the normal collision processing
def handle_block_ground_collision(arbiter, space, data):
    block_shape = arbiter.shapes[1]
    block_body = block_shape.body

    # Check if the block is falling
    falling_threshold = 200  # A threshold velocity to consider the block as falling
    if block_body.velocity.y > falling_threshold:
        # The block is falling, so remove it from the space
        space.remove(block_shape, block_shape.body)
        block_body.is_intact = False

    return True
def handle_block_block_collision(arbiter, space, data):
    """Callback function to handle block-block collision."""
    block_shape_1 = arbiter.shapes[0]  # The first block in the collision pair
    block_shape_2 = arbiter.shapes[1]  # The second block in the collision pair

    block_body_1 = block_shape_1.body
    block_body_2 = block_shape_2.body

    # Check if either block is falling with high velocity
    falling_threshold = 400  # A threshold velocity to consider a block falling

    if block_body_1.velocity.y > falling_threshold:
        # The first block breaks, so remove it from the space
        space.remove(block_shape_1, block_body_1)
        block_body_1.is_intact = False

    # Check if the second block is falling or rotating too fast
    elif block_body_2.velocity.y > falling_threshold:
        # The second block breaks, so remove it from the space
        space.remove(block_shape_2, block_body_2)
        block_body_2.is_intact = False

    return True  # Continue with the normal collision processing
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
def draw_rubber_band(screen, bird_pos, dragging):
    rubber_band_color = (50, 30, 30)  # Dark brown for the rubber band
    rubber_band_thickness = 8

    # Draw the rubber band only if the bird is being dragged
    if not bird_launched:
        # Left rubber band
        pygame.draw.line(screen, rubber_band_color, left_band_anchor, bird_pos, rubber_band_thickness)
        #Right rubber band
        pygame.draw.line(screen, rubber_band_color, right_band_anchor, bird_pos, rubber_band_thickness)
def level(block_list, levels):
    if len(block_list) > 0:
        return True
    elif len(block_list) == 0:
        levels.remove(block_list)
        if levels:
            for block1 in levels[0]:
                block1.created = True
                space.add(block1, block1.shape)
        else:
            # No more levels, handle accordingly
            print("Congratulations! You've completed all levels.")

bird = create_bird(*slingshot_pos)

block_list = [blocks(800, 730, 50, 100, True, True), blocks(900, 730, 50, 100, True, True), blocks(800, 685, 100, 50, True, True),
              blocks(900, 685, 100, 50, True, True), blocks(800, 535, 50, 100, True, True), blocks(900, 535, 50, 100, True, True),
              blocks(800, 460, 100, 50, True, True), blocks(900, 460, 100, 50, True, True)]

block_list1 = [blocks(800, 340, 50, 100, True, False), blocks(900, 340, 50, 100, True, False), blocks(800, 730, 50, 100, True, False),
               blocks(900, 730, 50, 100, True, False), blocks(800, 685, 100, 50, True, False), blocks(900, 685, 100, 50, True, False),
               blocks(800, 535, 50, 100, True, False), blocks(900, 535, 50, 100, True, False), blocks(800, 460, 100, 50, True, False),
               blocks(900, 460, 100, 50, True, False)]

block_list2 = [blocks(800, 290, 100, 50, True, False), blocks(900, 290, 100, 50, True, False), blocks(800, 240, 50, 100, True, False),
               blocks(900, 340, 50, 100, True, False), blocks(800, 730, 50, 100, True, False), blocks(900, 730, 50, 100, True, False),
               blocks(800, 685, 100, 50, True, False), blocks(900, 685, 100, 50, True, False), blocks(800, 535, 50, 100, True, False),
               blocks(900, 535, 50, 100, True, False), blocks(800, 460, 100, 50, True, False), blocks(900, 460, 100, 50, True, False)]

levels = [block_list, block_list1, block_list2]

# Add a collision handler for bird-block collisions
collision_handler = space.add_collision_handler(BIRD_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
collision_handler.begin = handle_bird_block_collision  # Set the callback

block_ground_collision_handler = space.add_collision_handler(GROUND_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_ground_collision_handler.begin = handle_block_ground_collision  # Set the callback

# Add a collision handler for block-block collisions
block_block_collision_handler = space.add_collision_handler(BLOCK_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_block_collision_handler.begin = handle_block_block_collision  # Set the callback

# Define rubber band attachment points on the slingshot
left_band_anchor = (65, 620)  # Left side of the slingshot
right_band_anchor = (135, 620)  # Right side of the slingshot

# Function to draw the rubber band of the slingshot

# Main loop
running = True
dragging = False
launch_power = 100
initial_mouse_pos = None  # Store initial click position
bird_launched = False  # Track whether the bird has been launched
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                dragging = False
                launch_power = 100
                initial_mouse_pos = None  # Store initial click position
                bird_launched = False  # Track whether the bird has been launched
                bird.position = slingshot_pos
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
                bird_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/BirdFlying1.png")  # Path to your uploaded image

    # Keep the bird floating until launched
    if not bird_launched and not dragging:
        bird.velocity = (0, 0)  # Ensure bird stays in place until launched
        bird.position = slingshot_pos  # Reset bird position to the slingshot

    screen.fill((200, 220, 255))  # Blue background (sky)

    # Update physics
    space.step(1 / 50.0)  # Simulate physics with a fixed time step
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

    draw_rubber_band(screen, bird.position, dragging)

    draw_bird(screen, bird)

    level(levels[0], levels)

    # Use a copy of the list to avoid issues when removing items
    for block in levels[0][:]:
        if block.is_intact:
            draw_blocks(screen, block)
        else:
            levels[0].remove(block)


    pygame.display.flip()
    clock.tick(50)

pygame.quit()
