import pygame
import pymunk
import pymunk.pygame_util

# Initialize Pygame and Pymunk
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Angry Birds in Python")
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 900)

# Draw options
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create ground and bird
def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (400, 590)
    shape = pymunk.Segment(body, (-400, 0), (400, 0), 5)
    shape.elasticity = 0.4
    space.add(body, shape)
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
def slingshot_box(x):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (100, 400) #kjhgf
    shape = pymunk.Segment(body, (x, 0), (x+100, 0), 5)
    shape2 = pymunk.Segment(body, (x+100, 0), (x+100, 100), 5)
    shape3 = pymunk.Segment(body, (x, 100), (x+100, 100), 5)
    shape4 = pymunk.Segment(body, (x, 100), (x, 0), 5)



    space.add(body, shape, shape2, shape3, shape4)

create_ground()
bird = create_bird(100,500)
slingshot_box(10)

# Main game loop
running = True
dragging = False
launch_power = 20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bird.position.get_distance(pygame.mouse.get_pos()) < 20:
                dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_pos = pygame.mouse.get_pos()
                launch_velocity = (bird.position - mouse_pos) * -launch_power
                bird.velocity = launch_velocity
                dragging = False
    if dragging:
        position_x, position_y = bird.position
        bird.position = pygame.mouse.get_pos()


    # Update physics
    space.step(1/60)

    # Clear screen and draw everything
    screen.fill((135, 206, 235))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
