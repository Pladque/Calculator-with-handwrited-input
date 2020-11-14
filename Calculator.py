import os
import tensorflow as tf
import keras
import pygame, random
import numpy as np
from consts import BLUE, BLACK, OPERATORS, GREEN, WHITE
from ExtractSingeSignFromInput import SeperateDigids, FillEmptySpaceInSeperatedDigits
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
pygame.init()

# setting up the screen #
clock = pygame.time.Clock()
PLAY_SPEED = 120
WIDTH = 800
HEIGHT = 200
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill((BLUE))
pygame.display.set_caption('Calculator')

class Display:

    def __init__(self, text, center, size):
        self.font = pygame.font.Font('freesansbold.ttf', size) 
        self.text = self.font.render(text, True, BLACK) 
        self.textRect = self.text.get_rect() 
        self.textRect.center = center

    def Show(self, result):
        self._reset()
        self.text = self.font.render('=' + str(result), True, BLACK) 
        screen.blit(self.text, self.textRect)

    def _reset(self):
        self.text = self.font.render('           ', True, BLACK, BLUE) 
        screen.blit(self.text, self.textRect)

def calculate(num1, num2, operator):        
    if operator == '+':
        return num1+num2
    if operator == '*':
        return num1 * num2
    if operator == '/':
        if num2 != 0:
            return num1 / num2
        else: return '?'
    if operator == '-':
        return num1 - num2
    else:
        return str(num1)+str(operator)+str(num2)

def draw_on_grid():
    mx, my = pygame.mouse.get_pos()
    for box in boxes:
        if pygame.mouse.get_pressed()[0] and abs(mx - box[1]) < INPUT_DETECT_RANGE and abs(my - box[2]) < INPUT_DETECT_RANGE:
            box[0] = DRAW_COLOR
            pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

def reset_grid():
    for box in boxes:
        box[0] = BOARD_COLOR
        pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

def guess(li, probably_operator):
    if li != []:
        if probably_operator is False:
            model = tf.keras.models.load_model('equation_reader.model')
            predictions = model.predict(li)
            t = np.argmax(predictions[0])
            temp = list(predictions[0])
            while t>=10:
                for x, pred in enumerate(temp):
                    if x == t:  temp.pop(x)
                temp = np.array(temp)
                t = np.argmax(temp)
            print("I predict this number is a:", t)

        else: 
            model = tf.keras.models.load_model('equation_reader.model')
            predictions = model.predict(li)
            t = np.argmax(predictions[0])
            temp = list(predictions[0])
            while t<10: 
                for x, pred in enumerate(temp):
                    if x == t:  temp.pop(x)
                temp = np.array(temp)
                t = np.argmax(temp)

            t = OPERATORS[t - 10]
            print('I think it is: ', t)

        return t
    else: return []

# Setting up the grid
DRAW_COLOR = BLACK
BOARD_COLOR = BLUE

display = Display('=', (670, 100), 72)
display.Show('')

BOX_SIZE = 10
INPUT_DETECT_RANGE = BOX_SIZE/2 + 1

boxes = []
FILLED = False
BOARD_WIDTH = WIDTH - 200
for x in range(int(WIDTH/BOX_SIZE)):
    for y in range(int(HEIGHT/BOX_SIZE)):
        boxes.append( [BOARD_COLOR, x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE])      
for box in boxes:
    pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)
    
if __name__ == '__main__':
    run = True

    while run:
        clock.tick(PLAY_SPEED)
        draw_on_grid()
         

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # guessing input
                    covariates = []
                    for box in boxes:
                        if box[0] == DRAW_COLOR:
                            covariates.append(1)
                        else: covariates.append(0)
                        pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

                    covariates = np.array(covariates).transpose()
                    covariates = covariates.tolist()

                    seperated_digids = SeperateDigids(covariates, 20)

                    digids_as_ints = []
                    for x, digid in enumerate(seperated_digids):
                        seperated_digids[x] = FillEmptySpaceInSeperatedDigits(digid, 20, 20)

                        if x == 1:
                            digids_as_ints.append(guess([seperated_digids[x]], True))
                        else: digids_as_ints.append(guess([seperated_digids[x]], False))

                    result = calculate(digids_as_ints[0], digids_as_ints[2], digids_as_ints[1])
                    display.Show(result)

                if event.key == pygame.K_BACKSPACE:
                    reset_grid()
                    display.Show(' ')
                    
        pygame.display.flip()

pygame.quit()