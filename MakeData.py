import pygame, random
import numpy as np


RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

WIDTH = 600
HEIGHT = 200
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill(([255,255,255]))

FILLED = False

MAKING_TRAINING_DATA = True 
TRAINING_DATA_SIZE = 5
OPERATORS = ['+', '-', '*', '/']

boxes = []
BOX_SIZE = 10

for x in range(int(WIDTH/BOX_SIZE)):
    for y in range(int(HEIGHT/BOX_SIZE)):
        boxes.append( [BLUE, x*BOX_SIZE, y*BOX_SIZE, BOX_SIZE, [x,y]])      # last is ID for debug
        
for box in boxes:
    pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

expected_responses = []
covariates = [[]]
if MAKING_TRAINING_DATA:
    for i in range(TRAINING_DATA_SIZE):
        expected_responses.append([random.randint(0,10), OPERATORS[random.randint(0,3)], random.randint(0,10)])

    curr_input_index = 0
    print(expected_responses[curr_input_index])


run = True
input_detect_range = BOX_SIZE/2 + 1
while run:
    mx, my = pygame.mouse.get_pos()
    for box in boxes:
        if pygame.mouse.get_pressed()[0] and abs(mx - box[1]) < input_detect_range and abs(my - box[2]) < input_detect_range:
            box[0] = BLACK
            pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if curr_input_index < TRAINING_DATA_SIZE - 1:
                    # saving input
                    for box in boxes:
                        if box[0] == BLACK:
                            covariates[curr_input_index].append(1)
                        else: covariates[curr_input_index].append(0)
                        box[0] = BLUE
                        pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)

                    covariates[curr_input_index] = np.array(covariates[curr_input_index]).transpose()
                    covariates[curr_input_index] = covariates[curr_input_index].tolist()

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
                    print(expected_responses[curr_input_index])
                else: run = False
            if event.key == pygame.K_BACKSPACE:
                curr_input_index+=1
                print(expected_responses[curr_input_index])
                covariates.append([])
                for box in boxes:
                    box[0] = BLUE
                    pygame.draw.rect(screen, box[0],[box[1], box[2],box[3], box[3]], FILLED)


        
    pygame.display.flip()

pygame.quit()
