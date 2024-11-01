import pygame
import pymunk
import pymunk.pygame_util
import math
import random
import tkinter
from tkinter import *
from tkinter import simpledialog

root = tkinter.Tk()

class NoButtonDialog(simpledialog.Dialog):
    def body(self, master):
        tkinter.Label(master, text="Play Again? Click twice.").pack()
        return None
    def buttonbox(self):
        box = tkinter.Frame(self)

        no_button = tkinter.Button(box, text="No", width=10, command=self.no)
        no_button.pack(side=tkinter.LEFT, padx=5, pady=5)

        yes_button = tkinter.Button(box, text="Yes", width=10, command=self.yes)
        yes_button.pack(side=tkinter.LEFT, padx=5, pady=5)

        box.pack()

    def no(self):
        self.result = "No"
        self.destroy()

    def yes(self):
        self.result = "Yes"
        self.destroy()

def show_no_messagebox():
    root = tkinter.Tk()
    root.withdraw()  # Hide the main window
    dialog = NoButtonDialog(root)
    return dialog.result

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()


pygame.mixer.music.load('music.mp3')
rock_sound = pygame.mixer.Sound('rock_impact.mp3')
whoosh = pygame.mixer.Sound('whoosh.wav')
secret_song = pygame.mixer.Sound('secret.MP3')
jazz = pygame.mixer.Sound('chill_jazz.mp3')
pygame.mixer.music.set_volume(1.0)
rock_sound.set_volume(1.0)
sound_on = False  # Initially, the sound is off

# Set up the display
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

root.lift()
root.focus_force()

root.title("Level Select")
root.geometry("480x320+500+300")  # width x height + x + y

class Bear:
    def __init__(self, x, y):
        self.image = pygame.image.load('cuteBear.png')  # Load bear button image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

bird_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/BirdImage.png")  # Path to your uploaded image
bird_rect = bird_image.get_rect()

poof_1 = pygame.image.load("Poof1.png")
poof_2 = pygame.image.load("Poof2.png")
poof_3 = pygame.image.load("Poof3.png")

explode_1 = pygame.image.load("Explode1.png")
explode_1 = pygame.transform.scale(explode_1, (300,300))
explode_2 = pygame.image.load("Explode2.png")
explode_2 = pygame.transform.scale(explode_2, (300,300))
explode_3 = pygame.image.load("Explode3.png")
explode_3 = pygame.transform.scale(explode_3, (300,300))

bear_button = pygame.Rect( 10, 10, 100, 100)  # Rect for bear button (x, y, width, height)
bear_img = pygame.image.load('cuteBear.png')  # Use a bear image file here
bear_img = pygame.transform.scale(bear_img, (100, 100))  # Scale it to fit the button
music_playing = False  # Music starts off
hit_bird_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/BirdHit.png")

cloud_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/cloud.png")
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

medium_block = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/""MedBlock.png")
medium_block = pygame.transform.scale(medium_block, (100,50))
medium_block_hit_1 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/""MedBlockHit1.png")
medium_block_hit_1 = pygame.transform.scale(medium_block_hit_1, (100,50))
medium_block_hit_2 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/""MedBlockHit2.png")
medium_block_hit_2 = pygame.transform.scale(medium_block_hit_2, (100,50))
medium_block_hit_3 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/""MedBlockHit3.png")
medium_block_hit_3 = pygame.transform.scale(medium_block_hit_3, (100,50))
block_sprites = [medium_block, medium_block_hit_1, medium_block_hit_2, medium_block_hit_3]

pig_image = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/Pig.png")
pig_image_hit_1 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/PigHit1.png")
pig_image_hit_2 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/PigHit2.png")
pig_image_hit_3 = pygame.image.load("/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/PigHit3.png")
pig_sprites = [pig_image, pig_image_hit_1, pig_image_hit_2, pig_image_hit_3]

# Set up the space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity

slingshot_pos = (100, 600)  # Starting point of the bird (slingshot center)
max_drag_distance = 100     # Max distance allowed for dragging (circle radius)
level_num = 0
medium_block_num = 0
pig_image_num = 0

# Collision types
BIRD_COLLISION_TYPE = 1
BLOCK_COLLISION_TYPE = 2
GROUND_COLLISION_TYPE = 3
PIG_COLLISION_TYPE = 4

def reset_game_state(space, levels, level_num):
    # Remove existing level objects from the space
    for block in levels[level_num - 2][0]:  # Previous level's blocks
        if block.created:
            space.remove(block, block.shape)
            block.created = False
    for pig in levels[level_num - 2][1]:  # Previous level's pigs
        if pig.created:
            space.remove(pig, pig.shape)
            pig.created = False
    # Reset bird state
    while birds:
        birds.remove(birds[0])

    bird = create_bird(100, 600, (0, 0))

    bird_2 = create_bird(200, 750, (0, 0))
    bird_3 = create_bird(250, 750, (0, 0))

    birds.append(bird)
    birds.append(bird_2)
    birds.append(bird_3)

    global bird_launched
    bird_launched = False
    bird.position = slingshot_pos  # Reset bird position if needed
    bird.velocity = (0, 0)  # Stop any motion from the bird

    # Load the new level
    load_level(levels, level_num)
def load_level(levels, level_num1):
    if levels:
        for block1 in levels[level_num1-1]:
            for thing in block1:
                thing.created = True
                space.add(thing, thing.shape)
    else:
        # No more levels, handle accordingly
        print("Congratulations! You've completed all levels.")
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
    block_body.image = medium_block
    block_body.medium_block_num = medium_block_num

    block_body.is_intact = is_intact
    block_body.created = created
    block_body.shape = block_shape

    # Add the body and shape to the space
    if created:
        space.add(block_body, block_shape)

    return block_body
def draw_blocks(screen, block_body):
    if block_body.is_intact and block_body.medium_block_num < len(block_sprites):
        block_position = block_body.position
        block_angle_degrees = math.degrees(block_body.angle)

        # Determine whether to draw the block normally or rotated
        if block_body.width > block_body.height:
            # Draw normally
            rotated_block_image = pygame.transform.rotate(block_sprites[block_body.medium_block_num], -block_angle_degrees)
        else:
            # Draw rotated 90 degrees
            rotated_block_image = pygame.transform.rotate(block_sprites[block_body.medium_block_num], -block_angle_degrees + 90)

        rotated_rect = rotated_block_image.get_rect(center=(block_position.x, block_position.y))

        screen.blit(rotated_block_image, rotated_rect.topleft)
def pig(x, y, dead, created):
    mass = 0.1
    radius = 15
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    pig_body = pymunk.Body(mass, inertia)
    pig_body.position = (x, y)
    pig_shape = pymunk.Circle(pig_body, radius)
    pig_shape.elasticity = 0.8
    pig_shape.collision_type = PIG_COLLISION_TYPE
    pig_shape.friction = 1.0
    pig_body.velocity = (0, 0)
    pig_body.dead = dead
    pig_body.image = pig_image
    pig_body.pig_image_num = 0
    pig_body.created = created
    pig_body.shape = pig_shape

    if created and not dead:
        space.add(pig_body, pig_shape)
    return pig_body
def draw_pigs(screen, pig_body):
    if not pig_body.dead and pig_body.pig_image_num < len(pig_sprites):
        pig_position = pig_body.position
        pig_angle_degrees = math.degrees(pig_body.angle)  # Convert angle to degrees for Pygame

        rotated_pig_image = pygame.transform.rotate(pig_sprites[pig_body.pig_image_num],
                                                     -pig_angle_degrees)  # Rotate image (negative for correct direction)

        rotated_rect = rotated_pig_image.get_rect(center=(pig_position.x - 5, pig_position.y))

        screen.blit(rotated_pig_image, rotated_rect.topleft)

block_list = [blocks(800, 730, 50, 100, True, False), blocks(900, 730, 50, 100, True, False), blocks(800, 685, 100, 50, True, False),
              blocks(900, 685, 100, 50, True, False), blocks(800, 535, 50, 100, True, False), blocks(900, 535, 50, 100, True, False),
              blocks(800, 460, 100, 50, True, False), blocks(900, 460, 100, 50, True, False)]
pig_list = [pig(500, 750, False, False)]
level_one = [block_list, pig_list]

block_list2 = [blocks(800, 340, 50, 100, True, False), blocks(900, 340, 50, 100, True, False), blocks(800, 730, 50, 100, True, False),
               blocks(900, 730, 50, 100, True, False), blocks(800, 685, 100, 50, True, False), blocks(900, 685, 100, 50, True, False),
               blocks(800, 535, 50, 100, True, False), blocks(900, 535, 50, 100, True, False), blocks(800, 460, 100, 50, True, False),
               blocks(900, 460, 100, 50, True, False)]
pig_list2 = [pig(850, 430, False, False)]
level_two = [block_list2, pig_list2]

block_list3 = [blocks(800, 290, 100, 50, True, False), blocks(900, 290, 100, 50, True, False), blocks(800, 240, 50, 100, True, False),
               blocks(900, 340, 50, 100, True, False), blocks(800, 730, 50, 100, True, False), blocks(900, 730, 50, 100, True, False),
               blocks(800, 685, 100, 50, True, False), blocks(900, 685, 100, 50, True, False), blocks(800, 535, 50, 100, True, False),
               blocks(900, 535, 50, 100, True, False), blocks(800, 460, 100, 50, True, False), blocks(900, 460, 100, 50, True, False)]
pig_list3 = [pig(500, 720, False, False), pig(850, 430, False, False)]
level_three = [block_list3, pig_list3]

block_list4 = [blocks(600, 700, 50, 100, True, False), blocks(700, 700, 50, 100, True, False), blocks(800, 700, 50, 100, True, False)
               , blocks(600, 600, 100, 50, True, False), blocks(700, 600, 100, 50, True, False), blocks(800, 600, 100, 50, True, False)]
pig_list4= [pig(600, 575, False, False), pig(675, 575, False, False), pig(750, 575, False, False), pig(825, 575, False, False)]
level_four = [block_list4, pig_list4]

block_list5 = [blocks(700, 700, 50, 100, True, False), blocks(800, 700, 50, 100, True, False), blocks(800, 600, 100, 50, True, False),
               blocks(700, 600, 100, 50, True, False), blocks(700, 550, 50, 100, True, False), blocks(800, 550, 50, 100, True, False),
               blocks(700, 500, 100, 50, True, False), blocks(800, 500, 100, 50, True, False)]
pig_list5= [pig(750, 720, False, False),pig(750, 570, False, False)]
level_five = [block_list5, pig_list5]

block_list6 = [blocks(600, 700, 50, 100, True, False), blocks(650, 700, 50, 100, True, False), blocks(700, 700, 50, 100, True, False),
               blocks(600, 600, 50, 100, True, False), blocks(650, 600, 50, 100, True, False), blocks(700, 600, 50, 100, True, False),
               blocks(600, 500, 50, 100, True, False), blocks(650, 500, 50, 100, True, False), blocks(700, 500, 50, 100, True, False),
               blocks(600, 400, 50, 100, True, False), blocks(650, 400, 50, 100, True, False), blocks(700, 400, 50, 100, True, False),
               blocks(600, 300, 50, 100, True, False), blocks(650, 300, 50, 100, True, False), blocks(700, 300, 50, 100, True, False),
               blocks(600, 200, 50, 100, True, False), blocks(650, 200, 50, 100, True, False), blocks(700, 200, 50, 100, True, False),
               blocks(600, 100, 50, 100, True, False), blocks(650, 100, 50, 100, True, False), blocks(700, 100, 50, 100, True, False)]
pig_list6= [pig(900, 720, False, False)]
level_six = [block_list6, pig_list6]

block_list7 = [blocks(1000, 700, 100, 50, False, False)]
pig_list7= [pig(1000, 700, False, False)]
win = [block_list7, pig_list7]

levels = [level_one, level_two, level_three, level_four, level_five, level_six, win]

def on_button_click1():
    global level_num
    level_num = 1
    load_level(levels, level_num)
    root.destroy()
def on_button_click2():
    global level_num
    level_num = 2
    load_level(levels, level_num)
    root.destroy()
def on_button_click3():
    global level_num
    level_num = 3
    load_level(levels, level_num)
    root.destroy()
def on_button_click4():
    global level_num
    level_num = 4
    load_level(levels, level_num)
    root.destroy()
def on_button_click5():
    global level_num
    level_num = 5
    load_level(levels, level_num)
    root.destroy()
def on_button_click6():
    global level_num
    level_num = 6
    load_level(levels, level_num)
    root.destroy()

image = PhotoImage(file="/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/Level1.png") # TODO alter for differnt people
level_background_image = PhotoImage(file="/Users/kevin_francis/PycharmProjects/AngryBirdsPhysicsSim/LevelBackground.png") # TODO alter for differnt people

label1 = Label( root, image = level_background_image)
label1.place(x = 0, y = 0)

button = tkinter.Button(root, text="Click Me!", command=on_button_click1, image=image)
button.place(x=10, y = 10, width=image.width(), height= image.height())

button2 = tkinter.Button(root, text="Click Me!", command=on_button_click2, image=image)
button2.place(x=210, y = 10, width=image.width(), height= image.height())

button3 = tkinter.Button(root, text="Click Me!", command=on_button_click3, image=image)
button3.place(x=400, y = 10, width=image.width(), height= image.height())

button4 = tkinter.Button(root, text="Click Me!", command=on_button_click4, image=image)
button4.place(x=10, y = 110, width=image.width(), height= image.height())

button5 = tkinter.Button(root, text="Click Me!", command=on_button_click5, image=image)
button5.place(x=210, y = 110, width=image.width(), height= image.height())

button6 = tkinter.Button(root, text="Click Me!", command=on_button_click6, image=image)
button6.place(x=400, y = 110, width=image.width(), height= image.height())

root.mainloop()

# Create the ground as a static rectangle
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Static body
ground_body.position = (600, 780)  # Center of the screen horizontally, near the bottom

# Create the rectangular shape for the ground
ground_shape = pymunk.Poly.create_box(ground_body, (2200, 70))  # Width: 600, Height: 70
ground_shape.friction = 1.0
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
def draw_cloud(screen, x, y, scale=1.0):
    """Draws a cloud using a PNG at the specified position and scale."""
    # Scale the cloud image
    scaled_cloud = pygame.transform.scale(cloud_image, (int(cloud_rect.width * scale), int(cloud_rect.height * scale)))

    # Get the new rect of the scaled image to position it correctly
    scaled_rect = scaled_cloud.get_rect(center=(x, y))

    # Draw the cloud on the screen
    screen.blit(scaled_cloud, scaled_rect.topleft)
def draw_bird(screen, bird_body):
    bird_position = bird_body.position
    image1 = bird_body.image
    bird_angle_degrees = math.degrees(bird_body.angle)  # Convert angle to degrees for Pygame

    # Rotate the bird image based on the bird's angle
    rotated_bird_image = pygame.transform.rotate(image1, -bird_angle_degrees)  # Rotate image (negative for correct direction)

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
    bird_body.velocity = velocity
    bird_body.bird_launched = False
    bird_body.has_exploded = False
    bird_body.time = 100
    bird_body.image = bird_image
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
    pygame.draw.polygon(screen, shadow_color, [(80, 770), (50, 690), (35, 610), (45, 610), (62, 690)])  # Left arm

    # Add wood grain effect (lines for details)
    pygame.draw.line(screen, shadow_color, (95, 720), (95, 750), 2)  # Grain on the left side of the base
    pygame.draw.line(screen, shadow_color, (105, 720), (105, 750), 2)  # Grain on the right side of the base
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
def explode(space, bomb_position, radius=100, explosion_force=500):
    for body in space.bodies:
        distance = bomb_position.get_distance(body.position)
        if distance < radius:
            print("explode")
            # Calculate the force based on the distance and direction
            direction = body.position - bomb_position
            direction = direction.normalized()  # Get the unit vector
            force = explosion_force * (1 - distance / radius)
            body.apply_impulse_at_world_point(direction * force, body.position)
            birds[0].has_exploded = True
def handle_bird_block_collision(arbiter, space, data):
    """Callback function to handle bird-block collision."""
    block_shape = arbiter.shapes[1]  # The block is the second shape in the collision pair

    velocity_threshold = 100  # A threshold velocity to consider the block as falling

    # Remove the block's body and shape from the space
    if birds[0].velocity.y > velocity_threshold or birds[0].velocity.x > velocity_threshold:
        if Bird == 2 and not birds[0].has_exploded:
            print("HELLO")
            global explosion_timer
            explosion_timer = pygame.time.get_ticks()
            bomb_exploded = True
        block_shape.body.medium_block_num += 1
        if block_shape.body.medium_block_num >= len(block_sprites):
            space.remove(block_shape.body, block_shape)
            block_shape.body.created = False
    if bird.velocity.y > velocity_threshold or bird.velocity.x > velocity_threshold:
        block_shape.body.medium_block_num += 1
        if block_shape.body.medium_block_num >= len(block_sprites):
            space.remove(block_shape, block_shape.body)
            block_shape.body.is_intact = False
        else:
            block_shape.image = block_sprites[block_shape.body.medium_block_num]

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
    falling_threshold = 100  # A threshold velocity to consider the block as falling
    if block_body.velocity.y > falling_threshold or block_body.velocity.x > falling_threshold:
        block_shape.body.medium_block_num += 1
        if block_body.medium_block_num >= len(block_sprites):
            space.remove(block_shape, block_shape.body)
            block_body.is_intact = False
            block_body.created = False
        else:
            block_shape.image = block_sprites[block_body.medium_block_num]

    return True
def handle_block_block_collision(arbiter, space, data):
    """Callback function to handle block-block collision."""
    block_shape_1 = arbiter.shapes[0]  # The first block in the collision pair
    block_shape_2 = arbiter.shapes[1]  # The second block in the collision pair

    block_body_1 = block_shape_1.body
    block_body_2 = block_shape_2.body

    # Check if either block is falling with high velocity
    falling_threshold = 400  # A threshold velocity to consider a block falling

    if block_body_1.velocity.y > falling_threshold or block_body_1.velocity.x > falling_threshold:
        block_body_1.medium_block_num += 1
        if block_body_1.medium_block_num >= len(block_sprites):
            space.remove(block_body_1)
            block_body_1.is_intact = False
            block_body_1.created = False
        else:
            block_body_1.image = block_sprites[block_body_1.medium_block_num]

    # Check if the second block is falling or rotating too fast
    elif block_body_2.velocity.y > falling_threshold or block_body_2.velocity.x > falling_threshold:
        block_body_2.medium_block_num += 1
        if block_body_2.medium_block_num >= len(block_sprites):
            space.remove(block_body_2)
            block_body_2.is_intact = False
            block_body_2.created = False
        else:
            block_body_2.image = block_sprites[block_body_2.medium_block_num]

    return True  # Continue with the normal collision processing
def handle_bird_pig_collision(arbiter, space, data):
    pig_shape = arbiter.shapes[1]

    velocity_threshold = 1  # A threshold velocity to consider the block as falling

    # Remove the block's body and shape from the space
    if bird.velocity.y > velocity_threshold or bird.velocity.x > velocity_threshold:
        space.remove(pig_shape, pig_shape.body)
        pig_shape.body.dead = True

    # Collision handler to detect bird hitting block
    def bird_hit_pig(arbiter, space, data):
        global bird_image  # Modify global bird_image when the collision occurs
        bird_image = hit_bird_image  # Change bird's image to the new one
        return True  # Return True to process the collision

    # Add the collision handler
    handler = space.add_collision_handler(BIRD_COLLISION_TYPE, PIG_COLLISION_TYPE)
    handler.post_solve = bird_hit_pig  # Call bird_hit_block function when collision occurs

    return True  # Continue with the normal collision processing
def handle_pig_ground_collision(arbiter, space, data):
    pig_shape = arbiter.shapes[1]
    pig_body = pig_shape.body

    # Check if the block is falling
    falling_threshold = 1  # A threshold velocity to consider the block as falling
    if pig_body.velocity.y > falling_threshold or pig_body.velocity.x > falling_threshold:
        pig_shape.body.pig_image_num += 1
        if pig_body.pig_image_num >= len(pig_sprites):
            space.remove(pig_shape, pig_shape.body)
            pig_body.dead = True
        else:
            pig_shape.image = pig_sprites[pig_body.pig_image_num]

    return True
def handle_pig_block_collision(arbiter, space, data):
    block_shape = arbiter.shapes[0]  # The first block in the collision pair
    pig_shape = arbiter.shapes[1]  # The second block in the collision pair

    block_body = block_shape.body
    pig_body = pig_shape.body

    falling_threshold = 100  # A threshold velocity to consider a block falling

    if block_body.velocity.y > falling_threshold or block_body.velocity.x > falling_threshold:
        block_body.medium_block_num += 1
        if block_body.medium_block_num >= len(block_sprites):
            space.remove(block_body, block_shape)
            block_body.created = False
            block_body.is_intact = False
        else:
            block_body.image = block_sprites[block_body.medium_block_num]

    elif pig_body.velocity.y > falling_threshold or pig_body.velocity.x > falling_threshold:
        pig_body.pig_image_num += 1
        if pig_body.pig_image_num >= len(pig_sprites):
            space.remove(pig_body)
            pig_body.dead = True
        else:
            pig_body.image = pig_sprites[pig_body.pig_image_num]

    return True  # Continue with the normal collision processing

bird = create_bird(*slingshot_pos)

# Add a collision handler for bird-block collisions
collision_handler = space.add_collision_handler(BIRD_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
collision_handler.begin = handle_bird_block_collision  # Set the callback

block_ground_collision_handler = space.add_collision_handler(GROUND_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_ground_collision_handler.begin = handle_block_ground_collision  # Set the callback

# Add a collision handler for block-block collisions
block_block_collision_handler = space.add_collision_handler(BLOCK_COLLISION_TYPE, BLOCK_COLLISION_TYPE)
block_block_collision_handler.begin = handle_block_block_collision  # Set the callback

bird_pig_collision_handler = space.add_collision_handler(BIRD_COLLISION_TYPE, PIG_COLLISION_TYPE)
bird_pig_collision_handler.begin = handle_bird_pig_collision

pig_ground_collision_handler = space.add_collision_handler(GROUND_COLLISION_TYPE, PIG_COLLISION_TYPE)
pig_ground_collision_handler.begin = handle_pig_ground_collision

pig_block_collision_handler = space.add_collision_handler(BLOCK_COLLISION_TYPE, PIG_COLLISION_TYPE)
pig_block_collision_handler.begin = handle_pig_block_collision

def draw_bear_button():
    screen.blit(bear_img, (bear_button.x, bear_button.y))

# Define rubber band attachment points on the slingshot
left_band_anchor = (65, 620)  # Left side of the slingshot
right_band_anchor = (135, 620)  # Right side of the slingshot

# Set up the font and size
font = pygame.font.Font(None, 36)  # None loads default font, 36 is the font size
font2 = pygame.font.Font(None, 300)  # None loads default font, 36 is the font size

# Render text
text = font.render("Click 1 for Red", True, "red")  # True for anti-aliasing
text2 = font.render("Click 2 for The Blues", True, "blue")  # True for anti-aliasing
text3 = font.render("Click 3 for Bomb", True, "black")  # True for anti-aliasing
text4 = font.render("Click 4 for Chuck", True, "yellow")  # True for anti-aliasing
win = font2.render("YOU WIN", True, "black")  # True for anti-aliasing

# Get the text rectangle and position it
text_rect = text.get_rect(center=(200, 50))
text_rect2 = text2.get_rect(center=(420, 50))
text_rect3 = text3.get_rect(center=(670, 50))
text_rect4 = text4.get_rect(center=(900, 50))
win_rect = win.get_rect(center=(550, 400))

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                dragging = False
                launch_power = 100
                initial_mouse_pos = None  # Store initial click position
                bird_launched = False  # Track whether the bird has been launched
                bird.position = slingshot_pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if bear_button.collidepoint(event.pos):  # If bear button is clicked
                if level_num == 5:
                    secret_song.play()
                elif level_num == 2:
                    jazz.play()
                elif music_playing:
                    pygame.mixer.music.stop()  # Stop the music
                else:
                    pygame.mixer.music.play(-1)  # Play the music indefinitely
                music_playing = not music_playing  # Toggle the music state

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
                    drag_vector = drag_vector.normalized() * max_drag_distance

                # Calculate launch velocity and apply it to the bird
                launch_velocity = -drag_vector.normalized() * (drag_vector.length / max_drag_distance * launch_power) *10
                bird.velocity = launch_velocity
                dragging = False
                bird_launched = True  # Set bird as launched after release
                initial_mouse_pos = None  # Store initial click position
                whoosh.play()
                bird_image = bird_fly_image
    if birds:
        if Bird == 0 and birds:
            birds[0].mass = 1
            for bird in birds:
                bird.image = red_bird_image
            hit_bird_image = red_hit_image
            bird_fly_image = red_fly_image
        elif Bird == 1 and birds:
            birds[0].mass = 1
            for bird in birds:
                bird.image = blue_bird_image
            hit_bird_image = blue_hit_image
            bird_fly_image = blue_fly_image
        elif Bird == 2 and birds:
            birds[0].mass = 5
            for bird in birds:
                bird.image = bomb_bird_image
            hit_bird_image = bomb_hit_1_image
            bird_fly_image = bomb_fly_image
        elif Bird == 3 and birds:
            birds[0].mass = 1
            for bird in birds:
                bird.image = chuck
            hit_bird_image = chuck_hit
            bird_fly_image = chuck_fly
        # Keep the bird floating until launched
        if not birds[0].bird_launched and not dragging:
            for bird in birds:
                bird.velocity = (0,0)
            birds[0].position = slingshot_pos  # Reset bird position to the slingshot
        if birds[0].position.x > 1300 or birds[0].position.x < -100:
            try:time.sleep(1)
            except Exception: print("sleep no work")
            space.remove(birds[0])
            birds.remove(birds[0])
            lives-=1
        for pig in levels[level_num-1][1]:
            if pig.position.x > 1300:
                space.remove(pig)
                levels[level_num-1][1].remove(pig)
        for block in levels[level_num-1][1]:
            if block.position.x > 1200:
                space.remove(block, block.shape)
                block.created = False

        screen.fill((200, 220, 255))  # Blue background (sky)
        draw_bear_button()
        # Update physics
        try: space.step(1 / 50)  # Simulate physics with a fixed time step
        except Exception: print("THE SPACE DIDNT STEP")

        # Update the bird's position while dragging
        if dragging and birds:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_mouse_pos = pymunk.Vec2d(mouse_x, mouse_y)  # Get current mouse position
            drag_vector = current_mouse_pos - initial_mouse_pos  # Calculate drag vector based on the initial click

            # Ensure we do not exceed max drag distance
            if drag_vector.length > max_drag_distance:
                drag_vector = drag_vector.normalized() * max_drag_distance

            # Set bird's position to slingshot position + drag vector
            birds[0].position = slingshot_pos + drag_vector  # Update bird's position based on the drag
            birds[0].velocity = (0, 0)  # Bird doesn't move while dragging

            # Draw the predicted trajectory while dragging
            draw_trajectory(screen, birds[0], drag_vector)
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
        for n in cloudList: draw_cloud(screen,cloud_pos[0],cloud_pos[1],0.1)

        if not level_num == 7:
            screen.blit(text, text_rect)
            screen.blit(text2, text_rect2)
            screen.blit(text3, text_rect3)
            screen.blit(text4, text_rect4)
        else: screen.blit(win, win_rect)

        # Draw the custom floor
        draw_floor(screen, ground_shape)

        # Draw the grass on top of the ground, and clouds
        draw_grass(screen, 40, ground_shape, (34, 139, 34))
        draw_grass(screen, 22, ground_shape, (4, 109, 4))
        draw_grass(screen, 0, ground_shape, (34, 139, 34))

        # Draw bear button for sound control
        def draw_bear_button():
            screen.blit(bear_img, (bear_button.x, bear_button.y))

        current_time = pygame.time.get_ticks()

        if birds and Bird == 2 and bomb_exploded and not birds[0].has_exploded:
            print("done")
            explode(space, birds[0].position)
            bomb_exploded = False

        for bird in birds:
            if bird.has_exploded:
                if bird.time > 98:
                    print("1")
                    bird.time = bird.time - 1
                elif 96 < birds[0].time <= 98:
                    print("2")
                    bird.image = explode_1
                    bird.time = bird.time - 1
                elif 94 < birds[0].time <= 96:
                    print("3")
                    bird.image = explode_2
                    bird.time = bird.time - 1
                elif 92 < birds[0].time <= 94:
                    print("4")
                    bird.image = explode_3
                    bird.time = bird.time - 1
                elif bird.time == 92:
                    print("opoof")
                    if birds:
                        birds.remove(bird)
                        space.remove(bird)

        if birds and Bird == 3 and chuck_power and birds[0].bird_launched:
            chuck_power = False
            bird_image = chuck_fast
            birds[0].velocity = (birds[0].velocity.x*1.5, birds[0].velocity.y)

        if birds and birds[0].bird_launched and birds[0].position.y > 700 and not Bird == 2:
            if birds[0].time > 8:
                birds[0].time = birds[0].time-1
                if Bird == 1:
                    bird1.time = bird1.time - 1
                    bird2.time = bird2.time - 1
            elif 6 < birds[0].time <= 8:
                birds[0].image = poof_1
                bird1.image = poof_1
                bird2.image = poof_1
                birds[0].time = birds[0].time - 1
                if Bird == 1:
                    bird1.time = bird1.time - 1
                    bird2.time = bird2.time - 1
            elif 4 < birds[0].time <= 6:
                birds[0].image = poof_2
                bird1.image = poof_2
                bird2.image = poof_2
                birds[0].time = birds[0].time - 1
                if Bird == 1:
                    bird1.time = bird1.time - 1
                    bird2.time = bird2.time - 1
            elif 2 < birds[0].time <= 4:
                birds[0].image = poof_3
                bird1.image = poof_3
                bird2.image = poof_3
                birds[0].time = birds[0].time - 1
                if Bird == 1:
                    bird1.time = bird1.time - 1
                    bird2.time = bird2.time - 1
            elif birds[0].time == 2:
                if birds:
                    birds.remove(birds[0])
                    space.remove(birds[0])
                    space.remove(bird1)
                    space.remove(bird2)

        # Draw the wooden slingshot with enhanced details
        draw_slingshot(screen)

        if birds: draw_rubber_band(screen, birds[0].position, dragging)
        for bird in birds: draw_bird(screen, bird)

        if blue_bird_draw and not bird1.time == 1:
            draw_bird(screen, bird1)
            draw_bird(screen, bird2)
        # Use a copy of the list to avoid issues when removing items
        for block in levels[level_num-1][:][0]:
            if block.is_intact:
                draw_blocks(screen, block)
            else:
                levels[level_num-1][0].remove(block)
        for pig in levels[level_num-1][:][1]:
            if not pig.dead:
                draw_pigs(screen, pig)
            else:
                rock_sound.play()  # Play the rock sound once
                levels[level_num-1][1].remove(pig)
    if not birds or (len(levels[level_num - 1][1]) == 0 and ((5, 5) > birds[0].velocity > (0, 0))):
        if show_no_messagebox() == "Yes":
            # Move to the next level
            level_num += 1
            # Clear old level objects and load new level
            reset_game_state(space, levels, level_num)
        if show_no_messagebox() == "No":
            running = False
    pygame.display.flip()
    clock.tick(50)

pygame.quit()