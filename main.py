import pygame
import random
from math import sqrt
from pygame import mixer

# Initiallizing pygame
pygame.init()

# Creating the screen (x, y)
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
# Setting up the icon in a variable
icon = pygame.image.load("halloween.png")
# Setting the actual window icon to the icon variable
pygame.display.set_icon(icon)

# Background

background = pygame.image.load('space.jpg')

# Background sound, music is louder sound is shorter
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player image
playerImg = pygame.image.load('space_invaders ship.png')

# X coordinates, 0, 800 left to right
playerX = 370
# Y coordinate, lowest part of the screen is 600 pixels top to bottom
playerY = 480
# Variable for the change in x coordinate when arrow key is pressed
playerX_change = 0

# Bullet
bulletImg = pygame.image.load("weapons.png")
bulletX = 0
# Spaceship starts at ship level
bulletY = 480
bulletX_change = 0
bulletY_change = 10
# State of the bullet, ready is when it is not showing and in the ship, fired is when it has already been fired
# Ready - you can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_state = "ready"

# Enemy
# Creating lists for the enemies, because there will be multiple
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
# Number of enemies
num_of_enemies = 6
# For loop to place each value into the corresponding lists by apending them
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    # Will the method inside rand, randit to get a random integer between two numbers. Will have a random respawn
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 200))
    # Giving the initial speed of the enemy, making it randomly either negative or positive
    enemyX_change.append(4)
    """if enemyX_change == 0:
        enemyX_change = 5"""
enemyY_change = 40

# Checks if the change value is negative/positive then it will add or subtract 0.7 accordingly, or if its 0 it will set it to 0.3.
"""if enemyX_change == 1:
    enemyX_change -= .7
if enemyX_change == -1:
    enemyX_change += .7"""
if enemyX_change == 0:
    enemyX_change = 5

enemyY_change = 40
'''enemyY_change = random.randint(-1, 1)
if enemyY_change == 0:
    enemyY_change = .3'''


# Function for player
def player(x, y):
    # The screen is known as the surface of the game, blit means it will play onto the surface. Method blit(), takes parametres of the image and the coordinates
    screen.blit(playerImg, (x, y))


# They are in the local scope so they won't be affected by the other x and y variables, i value so that we can know which one we are talking about
def enemy(x, y, i):
    # Adding the enemy to the screen
    screen.blit(enemyImg[i], (x, y))


# Function for the bullet firing
def fire_bullet(x, y):
    # Calling the global variable
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Function for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Finding the distance from the bullet to the enemy, using pythagorean theorem
    distance = sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    else:
        return False


# Score for the game

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def showscore(x, y):
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOverText():
    text = font.render("GAME OVER", True, (0, 0 ,0))
    screen.blit(text, (200, 0))

# Quit event variable
running = True
# Meat and potatoes of the program, an event is anything happening in the game window
while running:
    # RBG- Red, Green, BLue (0-255)
    screen.fill((0, 0, 0))
    # Draw the background screen after the black screen so it doesn't fill it
    screen.blit(background, (0, 0))

    # Checks through all the events happening, any event is something that happens in the game window, therefore you must check for it in the game window
    # todo Make an event where it is when the full screen button is pressed so it will match the screen length and width of your screen.
    for event in pygame.event.get():
        # If the event that happens in the window is a quit event or clicking on the X button it will set the quit event variable to False, breaking the loop
        if event.type == pygame.QUIT:
            running = False
        # Checks if any keystroke has been pressed, KEYDOWN is pressing the key and KEYUP is removal of the key, you can make a holding button feature with this
        if event.type == pygame.KEYDOWN:
            # If a key stroke is pressed checks if it left or right arrow, any key can be accessed by K_...
            if event.key == pygame.K_LEFT:
                # Changes the speed of the ship when the player holds the left key, negative speed to move left.
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                # Changes the speed when the player holds the right key positive speed to move right
                playerX_change = 3
            # Will check for event of space being pressed
            if event.key == pygame.K_SPACE:
                # Will only play if the bullet is not on the screen
                if bullet_state == "ready":

                    # Gets the current X value of the player ship and stays on that x coordinate until resetting
                    bulletX = playerX
                    # When the space bar is released the bullet sound is played
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # Resets the speed to 0 when the keystroke is up or when released.
                playerX_change = 0

    # After each iteration if the key is still being pressed down then it will move.
    playerX += playerX_change
    # If the spaceship reaches the border it will stop by setting its x coordinate back to 0
    if playerX < 0:
        playerX = 0
    # It's not stopping it its just making a new ship when it reaches the boundary.
    elif playerX >= 736:
        # We are setting it to 736 because the icon for the spaceship is 64 pixels wide, so it will reach the edge at 800 - 64 = 736.
        playerX = 736

    # Change the screen color of the window, it has to be in the while loop so it happens continously while the game is running

    # Player method must be called after fill because you want it at the very top of the surface
    player(playerX, playerY)

    # Adding the enemy to the screen
    # Enemy movement, goes through each enemies list one by one
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOverText()
            break
        enemyX[i] += enemyX_change[i]
        # Checking for boundries
        if enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change
        elif enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change
        # If collision is true, we must reset the enemy and the bullet, program needs to know what enemy we are talking about.
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletY = 480
            bullet_state = "ready"
            # Increases the score by 1
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 200)
        # Adds the enemy to the screen, using its position and its i number in the list
        enemy(enemyX[i], enemyY[i], i)
    # If bullet reaches edge it will reset
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    showscore(textX, textY)
    # Update the screen with new things
    pygame.display.update()
