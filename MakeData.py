import pygame, random
import numpy as np
from consts import BLUE, BLACK, OPERATORS, GREEN, BLUE, WHITE, bcolors
from ExtractSingeSignFromInput import SeperateDigids, FillEmptySpaceInSeperatedDigits

pygame.init()

def reset_grid():
    for box in boxes:
        box[0] = BOARD_COLOR
        pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

def draw_on_grid():
    mx, my = pygame.mouse.get_pos()
    for box in boxes:
        if pygame.mouse.get_pressed()[0] and abs(mx - box[1]) < INPUT_DETECT_RANGE and abs(my - box[2]) < INPUT_DETECT_RANGE:
            box[0] = DRAW_COLOR
            pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

def show_expected_input_on_board(expected_responses):
    text = font.render(str(expected_responses[0])+" "+str(expected_responses[1])+" "+str(expected_responses[2]), True, WHITE) 
    textRect = text.get_rect() 
    textRect.center = (45, 15) 
    screen.blit(text, textRect) 

# setting up the screen #
clock = pygame.time.Clock()
PLAY_SPEED = 120
WIDTH = 600
HEIGHT = 200
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill(([255,255,255]))
pygame.display.set_caption('Data maker')

font = pygame.font.Font('freesansbold.ttf', 16) 

DRAW_COLOR = BLACK
BOARD_COLOR = BLUE

# Setting up the grid
boxes = []
BOX_SIZE = 10
FILLED = False
INPUT_DETECT_RANGE = BOX_SIZE/2 + 1
for x in range(int(WIDTH/BOX_SIZE)):
    for y in range(int(HEIGHT/BOX_SIZE)):
        boxes.append( [BOARD_COLOR, x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE])      
for box in boxes:
    pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

# getting random responses
MAKING_TRAINING_DATA = True
TRAINING_DATA_SIZE = 50
expected_responses = []
covariates = [[]]
if MAKING_TRAINING_DATA:
    for i in range(TRAINING_DATA_SIZE):
        expected_responses.append([random.randint(0,9), OPERATORS[random.randint(0,3)], random.randint(0,9)])
    curr_input_index = 0
    print(expected_responses[curr_input_index])

    show_expected_input_on_board(expected_responses[curr_input_index])
    
run = True
while run:
    clock.tick(PLAY_SPEED)

    draw_on_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if curr_input_index < TRAINING_DATA_SIZE - 1:
                    # saving input and reseting grid
                    for box in boxes:
                        if box[0] == DRAW_COLOR:
                            covariates[curr_input_index].append(1)
                        else: covariates[curr_input_index].append(0)
                        box[0] = BOARD_COLOR
                        pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

                    covariates[curr_input_index] = np.array(covariates[curr_input_index]).transpose()
                    covariates[curr_input_index] = covariates[curr_input_index].tolist()

                    # Saving data
                    with open("data.txt", 'a') as f:
                        f.write( ';'.join(map(str,expected_responses[curr_input_index])))

                        for x, covariate in enumerate(covariates[curr_input_index]):
                            if (x % 20 == 0): f.write('\n')
                            f.write(str(covariate))
                            f.write(';')


                        f.write('\n\n')

                        f.close()

                    covariates.append([])
                    curr_input_index+=1

                    print(curr_input_index, ':')
                    print(expected_responses[curr_input_index])

                    show_expected_input_on_board(expected_responses[curr_input_index])

                else: run = False
            if event.key == pygame.K_BACKSPACE:
                curr_input_index+=1
                print(expected_responses[curr_input_index])
                covariates.append([])
                reset_grid()
                show_expected_input_on_board(expected_responses[curr_input_index])
                
    pygame.display.flip()

pygame.quit()
