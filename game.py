from pygame import *

# --------------------
# INITIALIZATION
# --------------------
init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

window = display.set_mode(SIZE)
display.set_caption("Pac-Man Chase")

clock = time.Clock()

# --------------------
# IMAGES
# --------------------
background = transform.scale(
    image.load("imgs/background.png"),
    SIZE
)

pacmanSize = (100, 80)
ghostSize = (100, 80)

pacman = transform.scale(
    image.load("imgs/pacman.png"),
    pacmanSize
)

pinkghost = transform.scale(
    image.load("imgs/pinkghost.png"),
    ghostSize
)

yellowghost = transform.scale(
    image.load("imgs/yellowghost.png"),
    ghostSize
)

# --------------------
# PLAYER
# --------------------
pacmanPosx = 50
pacmanPosy = SCREEN_HEIGHT // 2
pacmanSpeed = 6
angle = 0

# --------------------
# PINK GHOST
# --------------------
pinkghostPosx = 700
pinkghostPosy = 100
pinkghostSpeed = 2

# --------------------
# YELLOW GHOST
# --------------------
yellowghostPosx = 400
yellowghostPosy = 300
yellowghostSpeed = 3

# --------------------
# PELLETS
# --------------------
pellets = [
    [100, 100],
    [200, 200],
    [300, 150],
    [400, 300],
    [500, 100],
    [600, 250],
    [700, 400],
    [800, 150]
]

score = 0

# --------------------
# FONTS
# --------------------
scoreFont = font.SysFont("Arial", 35)
messageFont = font.SysFont("Arial", 80)

# --------------------
# GAME LOOP
# --------------------
game = True
gameResult = ""

while game:

    # EVENTS
    for e in event.get():
        if e.type == QUIT:
            game = False

    # KEYBOARD
    keys = key.get_pressed()

    if keys[K_LEFT] and pacmanPosx > 0:
        pacmanPosx -= pacmanSpeed
        angle = 180

    if keys[K_RIGHT] and pacmanPosx < SCREEN_WIDTH - pacmanSize[0]:
        pacmanPosx += pacmanSpeed
        angle = 0

    if keys[K_UP] and pacmanPosy > 0:
        pacmanPosy -= pacmanSpeed
        angle = 90

    if keys[K_DOWN] and pacmanPosy < SCREEN_HEIGHT - pacmanSize[1]:
        pacmanPosy += pacmanSpeed
        angle = -90

    # DIAGONAL ROTATION
    if keys[K_LEFT] and keys[K_UP]:
        angle = 135
    elif keys[K_LEFT] and keys[K_DOWN]:
        angle = -135
    elif keys[K_RIGHT] and keys[K_UP]:
        angle = 45
    elif keys[K_RIGHT] and keys[K_DOWN]:
        angle = -45

    # --------------------
    # PINK GHOST CHASES PACMAN
    # --------------------
    if pinkghostPosx < pacmanPosx:
        pinkghostPosx += pinkghostSpeed
    elif pinkghostPosx > pacmanPosx:
        pinkghostPosx -= pinkghostSpeed

    if pinkghostPosy < pacmanPosy:
        pinkghostPosy += pinkghostSpeed
    elif pinkghostPosy > pacmanPosy:
        pinkghostPosy -= pinkghostSpeed

    # --------------------
    # YELLOW GHOST CHASES PACMAN
    # --------------------
    if yellowghostPosx < pacmanPosx:
        yellowghostPosx += yellowghostSpeed
    elif yellowghostPosx > pacmanPosx:
        yellowghostPosx -= yellowghostSpeed

    if yellowghostPosy < pacmanPosy:
        yellowghostPosy += yellowghostSpeed
    elif yellowghostPosy > pacmanPosy:
        yellowghostPosy -= yellowghostSpeed

    # --------------------
    # COLLISION RECTS
    # --------------------
    pacmanRect = Rect(
        pacmanPosx,
        pacmanPosy,
        pacmanSize[0],
        pacmanSize[1]
    )

    pinkRect = Rect(
        pinkghostPosx,
        pinkghostPosy,
        ghostSize[0],
        ghostSize[1]
    )

    yellowRect = Rect(
        yellowghostPosx,
        yellowghostPosy,
        ghostSize[0],
        ghostSize[1]
    )

    # --------------------
    # GAME OVER
    # --------------------
    if pacmanRect.colliderect(pinkRect) or pacmanRect.colliderect(yellowRect):
        gameResult = "GAME OVER"
        game = False

    # --------------------
    # DRAW BACKGROUND
    # --------------------
    window.blit(background, (0, 0))

    # --------------------
    # DRAW PELLETS
    # --------------------
    for pellet in pellets[:]:

        draw.circle(window, (255, 255, 0), pellet, 8)

        pelletRect = Rect(
            pellet[0] - 8,
            pellet[1] - 8,
            16,
            16
        )

        if pacmanRect.colliderect(pelletRect):
            pellets.remove(pellet)
            score += 10

    # --------------------
    # WIN CONDITION
    # --------------------
    if len(pellets) == 0:
        gameResult = "YOU WIN!"
        game = False

    # --------------------
    # DRAW CHARACTERS
    # --------------------
    rotatedPacman = transform.rotate(
        pacman,
        angle
    )

    window.blit(
        rotatedPacman,
        (pacmanPosx, pacmanPosy)
    )

    window.blit(
        pinkghost,
        (pinkghostPosx, pinkghostPosy)
    )

    window.blit(
        yellowghost,
        (yellowghostPosx, yellowghostPosy)
    )

    # --------------------
    # SCORE
    # --------------------
    scoreText = scoreFont.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    window.blit(scoreText, (20, 20))

    display.update()
    clock.tick(60)

# --------------------
# END SCREEN
# --------------------
window.blit(background, (0, 0))

resultText = messageFont.render(
    gameResult,
    True,
    (255, 255, 0)
)

window.blit(
    resultText,
    (
        SCREEN_WIDTH // 2 - resultText.get_width() // 2,
        SCREEN_HEIGHT // 2 - resultText.get_height() // 2
    )
)

display.update()
time.wait(3000)

quit()
