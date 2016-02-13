import pygame
import random

__version__ = '0.1'

pygame.init()

# Import all required assets
crash_sound = pygame.mixer.Sound('Crash.wav')
pygame.mixer.music.load('Four_on_the_Dancefloor.wav')
car_img = pygame.image.load('car.png')
pygame.display.set_icon(car_img)

# Set screen resolution
display_width = 400
display_height = 800

# Set up game colours
black = (50, 50, 50)
white = (255, 255, 255)
blue = (109, 132, 180)
bright_blue = (59, 89, 152)
red = (179, 71, 36)
bright_red = (255, 92, 53)
green = (163, 204, 41)
bright_green = (216, 255, 53)
block_color = (53, 115, 255)

# Set up game variables
game_name = 'Dodge This!'
pause = False
teleport = False
crashed = False
shared = False
score = 0
car_width = 32

# Set up pygame stuff
store_mouse_pos = (0, 0)
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(game_name)
clock = pygame.time.Clock()


def things_dodged(count):
    # Counts the players score while the game runs.
    font = pygame.font.Font('impact.ttf', 36)
    text = font.render(str(count), True, black)
    game_display.blit(text, (display_width/2, 15))


def things(thingx, thingy, thingw, thingh, color):
    # Things are the blocks that fall towards the player.
    pygame.draw.rect(game_display, (0, 104, 172), [thingx, thingy, thingw, thingh])
    pygame.draw.rect(game_display, color, [thingx, thingy, thingw-3, thingh-6])


def background(backx, backy, backw, backh, color):
    # Not sure what this does
    pygame.draw.rect(game_display, color, [backx, backy, backw, backh])


def car(x, y):
    # Takes the players x and y co-ordinates and displays the player image
    game_display.blit(car_img, (x, y))


def text_objects(text, font, color):
    # Used in message display
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color, size, vpos):
    # Takes a string input, and displays it at the center of the screen
    # at the vertical position (vpos).
    large_text = pygame.font.Font('impact.ttf', size)
    TextSurf, TextRect = text_objects(text, large_text, color)
    TextRect.center = ((display_width / 2), vpos)
    game_display.blit(TextSurf, TextRect)
    pygame.display.update()


def crash():
    # Set what happens when the play crashes
    pygame.mixer.music.stop()

    global score
    global crashed
    game_display.fill(black)
    crashed = True

    message_display('You Crashed!', white, 48, (display_height/2))

    message_display('Score: ' + str(score), white, 40, (display_height - (display_height / 4)))

    # While loop to keep the game open until the player selects a button
    while crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button('Retry',50,450,100,50,green,bright_green,game_loop,black)
        button('EXIT',250,450,100,50,red,bright_red,game_quit,black)

        pygame.display.update()
        clock.tick(60)


def game_quit():
    # Small function to call if the game needs to quit.
    pygame.quit()
    quit()


def button(msg, x, y, w, h, ic, ac, action, fc):
        # Takes input and creates a button:
        # msg(String), x and y(position to draw), w and h (width and height)
        # ic and ac(inactive color and active color), action(the function to perform
        # when clicked. fc(Font color for the button).
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # If the player enters the button, change the color
        # When clicked, perform action
        if (mouse[0] >= x and mouse[0] <= x + w) and (mouse[1] >= y and mouse[1] <= y + h):
            pygame.draw.rect(game_display, ac, (x,y,w,h))
            if click[0] == 1 and action != None:
                action()

        else:
            pygame.draw.rect(game_display, ic, (x,y,w,h))

        # Draw the text onto the button
        small_text = pygame.font.Font('impact.ttf',20)
        textSurf, textRect = text_objects(msg, small_text, fc)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        game_display.blit(textSurf, textRect)


def unpause():
    # Unpause the game. Pause the music, and show the mouse again.
    global pause
    global store_mouse_pos
    #pygame.mixer.music.unpause()
    pygame.mouse.set_visible(False)
    #pygame.mouse.set_pos(store_mouse_pos)
    pause = False


'''
def teleported():
    # Not currently used. Created as an experiment but not great experience

    pygame.mixer.music.pause()
    pygame.mouse.set_visible(True)
    global teleport
    teleport = True

    while teleport:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if teleport == True:
                mouse_button = pygame.mouse.get_pressed()
                if mouse_button[0]:
                    pygame.mouse.set_visible(False)
                    teleport = False
                    pygame.mixer.music.unpause()

        pygame.display.update()
        clock.tick(60)
'''


def paused():
    # Pauses the game
    #pygame.mixer.music.pause()

    global pause
    pause = True

    message_display('paused', black, 48, (display_height/2))

    # While loop to keep the game open until the player selects a button.
    # Player can also use the p key
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if pause == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        #pygame.mouse.set_pos(store_mouse_pos)
                        pygame.mouse.set_visible(False)
                        pause = False
                        #pygame.mixer.music.unpause()

        button('Continue', 50, 450, 100, 50, green, bright_green, unpause, black)
        button('EXIT', 250, 450, 100, 50, red, bright_red, game_quit, black)

        pygame.display.update()
        clock.tick(60)

def game_intro():
    # First screen of the game. Displays buttons to start, or quit.
    game_display.fill(white)
    global game_name
    intro = True

    message_display(game_name, black, 48, (display_height/2))

    message_display('press p to pause', black, 24, (display_height - (display_height / 4)))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button('GO!',50,450,100,50,green,bright_green,game_loop,black)
        button('EXIT',250,450,100,50,red,bright_red,game_quit,black)

        pygame.display.update()
        clock.tick(60)

def game_loop():
    # Start the game. Play music and set the mouse position to be in the center of the screen.
    pygame.mixer.music.play(-1)
    #pygame.mouse.set_pos(((display_width - car_width) / 2), (display_height - 100))

    global shared
    shared = False
    global score
    score = 0
    global pause

    changeg = 230
    changeb = 238

    thing_speed = 7
    thing_width = 100
    thing_height = 100
    thing_startx = random.randrange(0, (display_width - thing_width))
    thing_starty = -1200

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    global store_mouse_pos
                    store_mouse_pos = pygame.mouse.get_pos()
                    pygame.mouse.set_visible(True)
                    pause = True
                    paused()
            mouse_button = pygame.mouse.get_pressed()
            if mouse_button[0]:
                None # teleported() - Unused function

        pygame.mouse.set_visible(False)
        mouse = pygame.mouse.get_pos()
        x = mouse[0]
        y = mouse[1]

        pink = (255, changeg, changeb)

        game_display.fill(pink)

        pygame.draw.rect(game_display, red, (0, 0, 1, display_height))
        pygame.draw.rect(game_display, red, (display_width-1, 0, display_width, display_height))

        things(thing_startx,thing_starty,thing_width,thing_height,block_color)
        thing_starty += thing_speed

        car(x, y)
        things_dodged(score)

        #if x > (display_width - 33) or x < (display_width - display_width):
        #    pygame.mouse.set_visible(True)
        #    crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, (display_width - thing_width))
            score += 1
            thing_speed += 0.5
            if changeg >= 10:
                changeg -= 6
                changeb -= 4
            # thing_width += (dodged * 1.2)

        if y > thing_starty and y < (thing_starty + thing_height) or (y + car_width) > thing_starty and (y + car_width) < thing_starty + thing_height:
            if x > thing_startx and x < (thing_startx + thing_width) or (x + car_width) > thing_startx and (x + car_width) < thing_startx + thing_width:
                pygame.mouse.set_visible(True)
                pygame.mixer.Sound.play(crash_sound)
                crash()

        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
