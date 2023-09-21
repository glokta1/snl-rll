import pygame
import random
import math
import queue
import time as t
from agent import SNLAgent
from snlgym import SNLGym

# hyperparameters
learning_rate = 0.01
n_episodes = 100
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = 0.05

# defining our agent
snl_agent = SNLAgent(
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

snlgym = SNLGym(100)
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake And Ladder")

clock = pygame.time.Clock()

# some Variables
crashed = False
pause = True
size = 25
roll = False
DONE1 = False
moveOne = False

# colors used
back = (96, 107, 114)
forg = (255, 138, 119)
darkback = (53, 53, 53)
boardclr = (255, 199, 95)
boardclr2 = (255, 237, 203)
snkclr = (168, 187, 92)
ladclr = (195, 64, 54)
pla1clr = (0, 211, 255)
pla2clr = (255, 121, 191)


# after Win
def WINNER():
    pygame.draw.rect(gameDisplay, (back), (95, 95, 610, 410))
    pygame.draw.rect(gameDisplay, (darkback), (100, 100, 600, 400))
    pygame.draw.rect(gameDisplay, (back), (105, 105, 590, 390))
    smallText = pygame.font.SysFont("comicsansms", 90)
    textSurf, textRect = text_objects("GAME OVER", smallText, darkback)
    textRect.center = ((display_width // 2), (display_height // 2 - 100))
    gameDisplay.blit(textSurf, textRect)

    smallText = pygame.font.SysFont("comicsansms", 50)
    textSurf, textRect = text_objects("WINNER : ", smallText, darkback)
    textRect.center = ((display_width // 4 + 100), (display_height // 2 + 100))
    gameDisplay.blit(textSurf, textRect)

    smallText1 = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects("Hit Space to Play", smallText1, darkback)
    textRect.center = ((700), (580))
    gameDisplay.blit(textSurf, textRect)

    if turn == 1:
        pygame.draw.circle(
            gameDisplay,
            pla2.clr,
            ((3 * display_width // 4), (display_height // 2 + 100)),
            60,
        )
    elif turn == 2:
        pygame.draw.circle(
            gameDisplay,
            pla1.clr,
            ((3 * display_width // 4), (display_height // 2 + 100)),
            60,
        )
    temp = True
    while temp:
        global crashed, DONE1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
                temp = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global b
                    gameDisplay.fill(back)
                    b.__init__()
                    pla1.__init__(b, pla1clr, False)
                    pla2.__init__(b, pla2clr, True)
                    temp = False
                    DONE1 = False
        pygame.display.update()


# game Board Class
class board:
    def __init__(self):
        # board List
        self.boardarr = []
        count = 1

        # generate 2D Board  10 X 10
        for i in range(0, 10):
            temp = []
            for j in range(0, 10):
                x = j * 60
                y = i * 60
                temp.append((x, y, count))
                count += 1
            self.boardarr.append(temp)

        # genrate Random Ladders
        self.ladders = []
        self.countarr = [100, 1]
        nooflad = 4
        j = 0
        for i in range(nooflad):
            val = True
            while val:
                rand1 = [67, 45, 38, 47]
                rand2 = [96, 63, 16, 89]
                diff = rand1[j] - rand2[j]
                if diff > 10 or diff < -10:
                    if rand1[j] not in self.countarr and rand2[j] not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand1[j] == y[2]:
                        a = y
                    if rand2[j] == y[2]:
                        b = y

            self.ladders.append((a, b))
            j += 1

        j = 0
        # genrate Random Snakes
        noofsnk = 4
        self.snakes = []
        for i in range(noofsnk):
            val = True
            while val:
                # rand1 = random.randint(1, 100)
                rand1 = [98, 84, 74, 68]
                # rand2 = random.randint(1, 100)
                rand2 = [3, 12, 46, 49]
                diff = rand1[j] - rand2[j]
                if diff > 10 or diff < -10:
                    if rand1[j] not in self.countarr and rand2[j] not in self.countarr:
                        val = False
                        self.countarr.append(rand1)
                        self.countarr.append(rand2)
            a = None
            b = None
            for x in self.boardarr:
                for y in x:
                    if rand1[j] == y[2]:
                        a = y
                    if rand2[j] == y[2]:
                        b = y
            self.snakes.append([a, b])
            j += 1

    def draw(self):
        for i in self.boardarr:
            for j in i:
                if int(j[2]) % 2 == 0:
                    colorb = boardclr
                else:
                    colorb = boardclr2

                pygame.draw.rect(gameDisplay, (colorb), (j[0], j[1], 59, 59))
                smallText = pygame.font.SysFont("comicsansms", 20)
                textSurf, textRect = text_objects(str(j[2]), smallText, darkback)
                textRect.center = ((j[0] + (60 // 2)), (j[1] + (60 // 2)))
                gameDisplay.blit(textSurf, textRect)
        for x in self.ladders:
            pygame.draw.line(
                gameDisplay,
                (ladclr),
                (x[0][0] + 20, x[0][1] + 30),
                (x[1][0] + 20, x[1][1] + 30),
                3,
            )
            pygame.draw.line(
                gameDisplay,
                (ladclr),
                (x[0][0] + 40, x[0][1] + 30),
                (x[1][0] + 40, x[1][1] + 30),
                3,
            )
        for x in self.snakes:
            pygame.draw.line(
                gameDisplay,
                (snkclr),
                (x[0][0] + 30, x[0][1] + 30),
                (x[1][0] + 30, x[1][1] + 30),
                8,
            )


# player class
class player:
    def __init__(self, B, clr, ai):
        self.val = 100
        self.xpos = None
        self.ypos = None
        self.ai = ai
        self.barr = B.boardarr
        self.lad = B.ladders
        self.snk = B.snakes
        self.clr = clr
        self.size = random.randint(15, 25)
        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    a = y
                    self.xpos = y[0]
                    self.ypos = y[1]

    def move(self, no):
        if self.ai:
            if (
                (self.val > 96)
                or (self.val <= 67 and self.val > 62)
                or (self.val > 38 and self.val < 45)
                or (self.val <= 16 and self.val > 14)
                or (self.val <= 9 and self.val > 5)
            ):
                no = 1
                print("The AI agent decided to move one space")
            else:
                no = random.randint(1, 6)
                print(f"The AI agent chose the mystery die and rolled a {no}")

        if self.val - no > 0:
            self.val -= no
        else:
            print("+=+" * 10 + " YOU WIN " + "+=+" * 10)
            global DONE1
            DONE1 = True

        for x in self.barr:
            for y in x:
                if self.val == y[2]:
                    a = y
                    self.xpos = y[0]
                    self.ypos = y[1]

        for l in self.lad:
            if (self.ypos == l[0][1] and self.xpos == l[0][0]) or (
                self.ypos == l[1][1] and self.xpos == l[1][0]
            ):
                if self.val == max(l[0][2], l[1][2]):
                    self.val = min(l[0][2], l[1][2])
                    for x in self.barr:
                        for y in x:
                            if self.val == y[2]:
                                a = y
                                self.xpos = y[0]
                                self.ypos = y[1]
                else:
                    pass

        for l in self.snk:
            if (self.ypos == l[0][1] and self.xpos == l[0][0]) or (
                self.ypos == l[1][1] and self.xpos == l[1][0]
            ):
                if self.val == min(l[0][2], l[1][2]):
                    self.val = max(l[0][2], l[1][2])
                    for x in self.barr:
                        for y in x:
                            if self.val == y[2]:
                                a = y
                                self.xpos = y[0]
                                self.ypos = y[1]
                else:
                    pass

        print(self.val)

    def draw(self):
        pygame.draw.circle(
            gameDisplay, (self.clr), (self.xpos + 30, self.ypos + 30), self.size
        )


def text_objects(text, font, clr, *kward):
    if len(kward) > 0:
        textSurface = font.render(text, True, clr, kward[0])
    else:
        textSurface = font.render(text, True, clr)
    return textSurface, textSurface.get_rect()


aimoves = [1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 2, 4, 6, 2, 2]
aiqueue = queue.Queue()
for move in aimoves:
    aiqueue.put(move)


# functions for dice
def one():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)


def two():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)


def three():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)


def four():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(
        gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size
    )


def five():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 2)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4))), size)
    pygame.draw.circle(
        gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4))), size
    )


def six():
    x, y, w, h = 605, 50, 190, 190
    pygame.draw.rect(gameDisplay, darkback, (x, y, w, h))
    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 2))), size)
    pygame.draw.circle(gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 2))), size)

    pygame.draw.circle(gameDisplay, forg, ((x + (w // 4)), (y + (h // 4)) - 10), size)
    pygame.draw.circle(
        gameDisplay, forg, ((x + (w // 4)), (y + (3 * h // 4)) + 10), size
    )
    pygame.draw.circle(
        gameDisplay, forg, ((x + (3 * w // 4)), (y + (h // 4)) - 10), size
    )
    pygame.draw.circle(
        gameDisplay, forg, ((x + (3 * w // 4)), (y + (3 * h // 4)) + 10), size
    )


# pygame Start

pygame.init()

b = board()
pla1 = player(b, (0, 211, 255), False)
pla2 = player(b, (255, 121, 191), True)
turn = 1
gameDisplay.fill(back)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                roll = True
            if event.key == pygame.K_o:
                moveOne = True

    if not DONE1:
        b.draw()
        pla1.draw()
        pla2.draw()
        smallText = pygame.font.SysFont("comicsansms", 40)
        textSurf, textRect = text_objects(str("Turn"), smallText, darkback, back)
        textRect.center = ((700), (300))
        gameDisplay.blit(textSurf, textRect)
        smallText1 = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(
            "Hit Space to roll the die", smallText1, darkback, back
        )
        textRect.center = ((700), (450))
        gameDisplay.blit(textSurf, textRect)
        textSurf, textRect = text_objects(
            "Hit O to move one space", smallText1, darkback, back
        )
        textRect.center = ((700), (500))
        gameDisplay.blit(textSurf, textRect)
        if turn == 1:
            if roll:
                # controls "dice roll" time. (5,6) indicates dice will cycle through 5 random numbers between 1-6 before arriving at a no
                time = random.randint(8, 10)
                for i in range(time):
                    no = random.randint(1, 6)  # range of dice numbers possible
                    if no == 1:
                        one()
                    elif no == 2:
                        two()
                    elif no == 3:
                        three()
                    elif no == 4:
                        four()
                    elif no == 5:
                        five()
                    elif no == 6:
                        six()
                    pygame.time.wait(100)
                    pygame.display.update()

                roll = False
                if turn == 1:
                    pla1.move(no)
                    turn = 2
                    pygame.draw.circle(gameDisplay, pla2.clr, (700, 400), 50)
                elif turn == 2:
                    pla2.move(no)
                    turn = 1
                    pygame.draw.circle(gameDisplay, pla1.clr, (700, 400), 50)
            if moveOne:
                if turn == 1:
                    one()
                    pla1.move(1)
                    turn = 2
                    pygame.draw.circle(gameDisplay, pla2.clr, (700, 400), 50)
                elif turn == 2:
                    pla2.move(1)
                    turn = 1
                    pygame.draw.circle(gameDisplay, pla1.clr, (700, 400), 50)
                moveOne = False
        else:
            # oneSurf, oneRect = text_objects(
            #     "Agent moved one space", smallText1, darkback, back
            # )
            # dieSurf, dieRect = text_objects(
            #     "Agent rolled the mystery die!", smallText1, darkback, back
            # )
            # oneRect.center = ((400), (300))
            # gameDisplay.blit(oneSurf, oneRect)
            # move = snl_agent.get_action(0, 0, False)
            # places = aiqueue.get()
            pla2.move(0)
            turn = 1

    else:
        WINNER()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
quit()
