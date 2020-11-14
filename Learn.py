import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from consts import OPERATORS, bcolors

WIDTH = 20
EXPECTED_HIGHT = 20
def load_data_signs(file_name, width, height):

    covariates = []
    expected_responses = []
    with open(file_name, 'r') as f:
        ind = -1
        for i, line in enumerate(f.readlines()):
            #print(i)
            if i % (height + 2) == 0:
                ind+=1
                expected_responses.append(line.split(';'))
                expected_responses[ind][-1] = expected_responses[ind][-1].replace('\n', '')
                for index, e_r in enumerate(expected_responses[ind]):
                    if '0'<=e_r <= '9':
                        expected_responses[ind][index] = int(e_r)
                    else: expected_responses[ind][index] = OPERATORS.index(e_r) + 10
                covariates.append([])
            else:
                line = line.split(';')
                for x, element in enumerate(line):
                    if '\n' in element:
                        if element == '\n':
                            line.pop(x)
                        else:
                            line[x] = line[x].replace('\n', '')

                for covariate in line:
                    covariates[ind].append(int(covariate))
        f.close() 
    return covariates, expected_responses    
    
if __name__ == '__main__':
    x_train, y_train = load_data_signs("digids_separated_data.txt", WIDTH, EXPECTED_HIGHT)

    # setting up the model 
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(14, activation=tf.nn.softmax))

    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=10)
    model.save('equation_reader.model')

    print(f"{bcolors.OKGREEN}","Model saved")

    