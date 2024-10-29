import pygame

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()

# Load the music and rock sound files
pygame.mixer.music.load('/sound/music.mp3')
rock_sound = pygame.mixer.Sound('rock_impact.mp3')

pygame.mixer.music.set_volume(1.0)  # Set music volume
rock_sound.set_volume(1.0)  # Set rock sound volume

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bear & Rock Sound Toggle")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button properties
bear_button = pygame.Rect(350, 250, 100, 100)  # Rect for bear button (x, y, width, height)
rock_button = pygame.Rect(500, 250, 100, 100)  # Rect for rock button

music_playing = False  # Music starts off
rock_playing = False  # Rock sound starts off

# Load bear button image
bear_img = pygame.image.load('cuteBear.png')  # Use a bear image file here
bear_img = pygame.transform.scale(bear_img, (100, 100))  # Scale it to fit the button

# Load rock button image
rock_img = pygame.image.load('Pig.png')  # Use a rock image file here
rock_img = pygame.transform.scale(rock_img, (100, 100))  # Scale it to fit the button

def draw_buttons():
    screen.blit(bear_img, (bear_button.x, bear_button.y))
    screen.blit(rock_img, (rock_button.x, rock_button.y))

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen
    draw_buttons()  # Draw the buttons

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bear_button.collidepoint(event.pos):  # If bear button is clicked
                if music_playing:
                    pygame.mixer.music.stop()  # Stop the music
                else:
                    pygame.mixer.music.play(-1)  # Play the music indefinitely
                music_playing = not music_playing  # Toggle the music state
            elif rock_button.collidepoint(event.pos):  # If rock button is clicked
                if rock_playing:
                    rock_sound.stop()  # Stop the rock sound
                else:
                    rock_sound.play()  # Play the rock sound once
                rock_playing = not rock_playing  # Toggle the rock sound state

    pygame.display.flip()  # Update the screen

pygame.quit()

# for block in levels[level_num - 1][:][0]:
#     if block.is_intact:
#         draw_blocks(screen, block)
#     else:
#         # Play the rock sound once
#         levels[level_num - 1][0].remove(block)
# for pig in levels[level_num - 1][:][1]:
#     if not pig.dead:
#         draw_pigs(screen, pig)
#     else:
#         rock_sound.play()  # Play the rock sound once
#         levels[level_num - 1][1].remove(pig)
# pygame.display.flip()