import pygame
import pymunk
import pymunk.pygame_util
import math
import random


# from pymunk.examples.planet import screen_size

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

pygame.mixer.music.load('/Users/jack_goode/PycharmProjects/AngryBirdsPhysicsSim/music.mp3')
pygame.mixer.music.set_volume(1.0)
sound_on = False  # Initially, the sound is off

# Set up the display
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)


class Bear:
    def __init__(self, x, y):
        self.image = pygame.image.load('cuteBear.png')  # Load bear button image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


bird_image = pygame.image.load("/Users/jack_goode/PycharmProjects/AngryBirdsPhysicsSim/BirdImage.png")  # Path to your uploaded image
bird_rect = bird_image.get_rect()
bear_button = pygame.Rect( 10, 10, 100, 100)  # Rect for bear button (x, y, width, height)
bear_img = pygame.image.load('cuteBear.png')  # Use a bear image file here
bear_img = pygame.transform.scale(bear_img, (100, 100))  # Scale it to fit the button
music_playing = False  # Music starts off
hit_bird_image = pygame.image.load("/Users/jack_goode/PycharmProjects/AngryBirdsPhysicsSim/BirdHit.png")

cloud_image = pygame.image.load("/Users/jack_goode/PycharmProjects/AngryBirdsPhysicsSim/cloud.png")
cloud_rect = cloud_image.get_rect()  # Get the dimensions of the cloud
# Cloud initial positions and velocities
cloud1_pos = [900, 0]  # x, y
cloud2_pos = [200, 120]
cloud3_pos = [600, 0]
cloudList = []
for n in range(5):
    # Initialize clouds with random x, y positions
    cloud_pos = [random.randint(0, screen.get_width()), random.randint(0, 150)]  # Randomize within a range
    cloudList.append(cloud_pos)
cloud_speed = 30  # Speed at which the clouds move (pixels per second)

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





# Function to draw the floor with a custom color
def draw_floor(screen, ground_shape):
    floor_color = (20, 200, 20)  # Custom color (green in this case)
    vertices = ground_shape.get_vertices()  # Get the vertices of the ground
    points = [(v.x + ground_body.position.x, v.y + ground_body.position.y) for v in vertices]
    pygame.draw.polygon(screen, floor_color, points)  # Draw the floor polygon

# Function to draw pointy grass
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


def draw_cloud(screen, x, y, scale=1.0):
    """Draws a cloud using a PNG at the specified position and scale."""
    # Scale the cloud image
    scaled_cloud = pygame.transform.scale(cloud_image, (int(cloud_rect.width * scale), int(cloud_rect.height * scale)))

    # Get the new rect of the scaled image to position it correctly
    scaled_rect = scaled_cloud.get_rect(center=(x, y))

    # Draw the cloud on the screen
    screen.blit(scaled_cloud, scaled_rect.topleft)



# Function to draw the bird image
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

# Function to create the bird
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

# Function to draw the sun with a smile and rays
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

# Function to draw the wooden slingshot with more detail
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
    pygame.draw.polygon(screen, shadow_color, [(80, 770), (50, 690), (35, 610), (45, 610), (62, 690)])  # Left arm

    # Add wood grain effect (lines for details)
    pygame.draw.line(screen, shadow_color, (95, 720), (95, 750), 2)  # Grain on the left side of the base
    pygame.draw.line(screen, shadow_color, (105, 720), (105, 750), 2)  # Grain on the right side of the base

def blocks(x, y, width, height):
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

    # Add the body and shape to the space
    space.add(block_body, block_shape)

    return block_body

def handle_bird_block_collision(arbiter, space, data):
    """Callback function to handle bird-block collision."""
    block_shape = arbiter.shapes[1]  # The block is the second shape in the collision pair

    velocity_threshold = 200  # A threshold velocity to consider the block as falling

    # Remove the block's body and shape from the space
    if bird.velocity.y > velocity_threshold:
        space.remove(block_shape, block_shape.body)

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

    # Check if the second block is falling or rotating too fast
    elif block_body_2.velocity.y > falling_threshold:
        # The second block breaks, so remove it from the space
        space.remove(block_shape_2, block_body_2)

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


bird = create_bird(*slingshot_pos)

blocks(800, 730, 50, 75)
blocks(900, 730, 50, 75)

blocks(800, 685, 100, 50)
blocks(900, 685, 100, 50)

blocks(800,535, 50, 75)
blocks(900,535, 50, 75)

blocks(800, 460, 100, 50)
blocks(900, 460, 100, 50)


# Add a collision handler for bird-block collisions
collision_handler = space.add_collision_handler(BIRD_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
collision_handler.begin = handle_bird_block_collision  # Set the callback

block_ground_collision_handler = space.add_collision_handler(GROUND_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_ground_collision_handler.begin = handle_block_ground_collision  # Set the callback

# Add a collision handler for block-block collisions
block_block_collision_handler = space.add_collision_handler(BLOCK_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_block_collision_handler.begin = handle_block_block_collision  # Set the callback

def draw_bear_button():
    screen.blit(bear_img, (bear_button.x, bear_button.y))


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
    draw_bear_button()  # Draw the bear button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if bear_button.collidepoint(event.pos):  # If bear button is clicked
                if music_playing:
                    pygame.mixer.music.stop()  # Stop the music
                else:
                    pygame.mixer.music.play(-1)  # Play the music indefinitely
                music_playing = not music_playing  # Toggle the music state
            # if bird.position.get_distance(mouse_pos) < 20 and not bird_launched:
            #     dragging = True
            #     bird.velocity = (0, 0)  # Stop any falling during drag
            #     initial_mouse_pos = mouse_pos  # Set initial mouse position when dragging starts
            #     if drag_vector.length > max_drag_distance:
            #         drag_vector = drag_vector.normalized() * max_drag_distance * 10
            #
            #
            #
            #     # Calculate launch velocity and apply it to the bird
            #     launch_velocity = -drag_vector.normalized() * (drag_vector.length / max_drag_distance * launch_power)
            #     bird.velocity = launch_velocity
            #     dragging = False
            #     bird_launched = True  # Set bird as launched after release
            #     initial_mouse_pos = None  # Store initial click position
            #     bird_image = pygame.image.load("/Users/jack_goode/PycharmProjects/AngryBirdsPhysicsSim/BirdFlying1.png")  # Path to your uploaded image
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if dragging and initial_mouse_pos and not bird_launched:
            #         mouse_x, mouse_y = pygame.mouse.get_pos()
            #         current_mouse_pos = pymunk.Vec2d(mouse_x, mouse_y)


                    # Keep the bird floating until launched
    if not bird_launched and not dragging:

        bird.velocity = (0, 0)  # Ensure bird stays in place until launched
        bird.position = slingshot_pos  # Reset bird position to the slingshot

    screen.fill((200, 220, 255))  # Blue background (sky)
    draw_bear_button()
    # Update physics
    space.step(1 / 50.0)  # Simulate physics with a fixed time step
    space.debug_draw(draw_options)

    # Draw the smiling sun in the background with rays
    draw_sun(screen)
    # Update the positions of the clouds
    cloud1_pos[0] += cloud_speed * (1 / 50.0)  # Speed * frame time
    cloud2_pos[0] += cloud_speed * (1 / 50.0)
    cloud3_pos[0] += cloud_speed * (1 / 50.0)
    i = 1
    for cloud_pos in cloudList:
        draw_cloud(screen, cloud_pos[0], cloud_pos[1], 0.2)# You can vary the scale if needed
        cloud_pos[0] += cloud_speed * (i/ 100.0)
        i+=1


    # Respawn clouds on the left side when they go off the right side of the screen
    if cloud1_pos[0] > 1700:
        cloud1_pos[0] = -800  # Respawn slightly off the screen on the left side
        cloud1_pos[1] = random.randint(-100, 150)  # Randomize the height for variety
    if cloud2_pos[0] > 1700:
        cloud2_pos[0] = -300
        cloud2_pos[1] = random.randint(-100, 150)
    if cloud3_pos[0] > 1700:
        cloud3_pos[0] = -300
        cloud3_pos[1] = random.randint(-100, 150)
    for n in cloudList:
        if cloud_pos[0] > 1700:
            cloud_pos[0] = -100

    # Draw moving clouds
    draw_cloud(screen, cloud1_pos[0], cloud1_pos[1], 0.3)
    draw_cloud(screen, cloud2_pos[0], cloud2_pos[1], 0.1)
    draw_cloud(screen, cloud3_pos[0], cloud3_pos[1], 0.1)
    for n in cloudList:
        draw_cloud(screen,cloud_pos[0],cloud_pos[1],0.1)




    # Draw the custom floor
    draw_floor(screen, ground_shape)

    # Draw the grass on top of the ground, and clouds
    draw_grass(screen, 40, ground_shape, (34, 139, 34))
    draw_grass(screen, 22, ground_shape, (4, 109, 4))
    draw_grass(screen, 0, ground_shape, (34, 139, 34))

    # Draw bear button for sound control
    def draw_bear_button():
        screen.blit(bear_img, (bear_button.x, bear_button.y))

    # Draw the wooden slingshot with enhanced details
    draw_slingshot(screen)

    draw_rubber_band(screen, bird.position, dragging)

    draw_bird(screen, bird)

    pygame.display.flip()
    clock.tick(50)


pygame.quit()