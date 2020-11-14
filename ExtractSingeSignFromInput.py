import numpy as np
from consts import bcolors

def ExtractSigns(file_name, width, height):
    covariates = []
    expected_responses = []
    with open(file_name, 'r') as f:
        ind = -1
        for i, line in enumerate(f.readlines()):
            if i % (height + 2) == 0:
                ind+=1
                expected_responses.append(line.split(';'))
                expected_responses[ind][-1] = expected_responses[ind][-1].replace('\n', '')
                covariates.append([])
            else:
                line = line.split(';')
                line.remove('\n')

                for covariate in line:
                    covariates[ind].append(covariate)
        f.close() 

    return covariates, expected_responses

def findNeighbors(arr, ind, connected_ones, width):        #return indexes of digit
    connected_ones.append(ind)

    if ind + width < len(arr) and arr[ind + width] == 1 and ind + width not in connected_ones:
        connected_ones += findNeighbors(arr, ind + width, connected_ones,width)

    if ind - width > 0 and arr[ind - width] == 1 and ind - width not in connected_ones:
        connected_ones += findNeighbors(arr, ind - width, connected_ones,width)

    if ind + width - 1 < len(arr) and arr[ind+ width - 1] == 1 and ind + width - 1 not in connected_ones and ind % width != 0:
        connected_ones += findNeighbors(arr, ind + width - 1, connected_ones,width)

    if ind+ width + 1 < len(arr) and arr[ind+ width + 1] == 1 and ind+ width + 1 not in connected_ones and (ind + 1) % width != 0:
        connected_ones += findNeighbors(arr, ind + width + 1, connected_ones,width)

    if ind - 1 > 0 and arr[ind - 1] == 1 and ind - 1 not in connected_ones and ind % width != 0:
        connected_ones += findNeighbors(arr, ind - 1, connected_ones,width)

    if ind + 1 < len(arr) and arr[ind + 1] == 1 and ind + 1 not in connected_ones and (ind + 1) % width != 0:
        connected_ones += findNeighbors(arr, ind + 1, connected_ones,width)

    if ind - width - 1 >= 0 and arr[ind - width - 1] == 1 and ind - width - 1 not in connected_ones and ind % width != 0:
        connected_ones += findNeighbors(arr, ind - width - 1, connected_ones,width)

    if ind - width + 1 >= 0 and arr[ind - width + 1] == 1 and ind - width + 1 not in connected_ones and (ind + 1) % width != 0:
        connected_ones += findNeighbors(arr, ind - width + 1, connected_ones,width)

    return list(dict.fromkeys(connected_ones))
        
def SeperateDigids(covariates, width):     #covariates is single input, its list, not list of lists

    seperated_digids = [[],[],[]]     #supporting up to 3 signs
    digid_indexes = [[],[],[]]
    
    sign_ind = 0
    neighbors = []
    for x,covariate in enumerate(covariates):
        if covariate == 1 and x not in seperated_digids[0] and x not in seperated_digids[1] and x not in seperated_digids[2]:
            try :
                seperated_digids[sign_ind] = findNeighbors(covariates, x, [], width)
            except: print("ERROR, Maby you draw more then 3 signs?")
            sign_ind += 1

    return seperated_digids

def FillEmptySpaceInSeperatedDigits(sign, width = 1, expected_height = 0):      # to make all inputs be same size
    try:
        max_min_diff = max(sign) - min(sign)
        output_arr_size = max_min_diff + ( max_min_diff% width) + 1  # +1 bc if there was olny 1 on arr, output_arr_size would be 0
        filled_sign_arr = []

        for _ in range(min(sign)%width):  filled_sign_arr.append(0)
        
        for _ in range(output_arr_size):
            if _ + min(sign) in sign:
                filled_sign_arr.append(1)
            else: filled_sign_arr.append(0)

        while len(filled_sign_arr) % width != 0:                filled_sign_arr.append(0)         
        while len(filled_sign_arr) < expected_height * width:   filled_sign_arr.append(0)
            
        return filled_sign_arr
    except ValueError: 
        print("Oops, it looks like some very unusual data: ")
        if sign == []: print("empty list!")
        return []

WIDTH = 20
HEIGHT = 60
EXPECTED_HIGHT = 20
if __name__ == '__main__':
    covariates, responses = ExtractSigns('data.txt', WIDTH, HEIGHT)

    seperated_digids = [[]]
    for x, group_of_covariates in enumerate(covariates):
        group_of_covariates = [int(covariate) for covariate in group_of_covariates]

        for digid in SeperateDigids(group_of_covariates, WIDTH):
            seperated_digids[x].append(FillEmptySpaceInSeperatedDigits(digid, width = WIDTH, expected_height = EXPECTED_HIGHT))
            seperated_digids.append([])

    with open("digids_separated_data.txt", 'w') as f:
        for inp_num, digids in enumerate(seperated_digids):
            for index, sign in enumerate(digids):
                f.write(responses[inp_num][index])
                for index, digid in enumerate(sign):
                    if index % WIDTH == 0:
                        f.write('\n')
                    f.write(str(digid)+';')
                f.write('\n\n')
        print(f"{bcolors.OKGREEN}","Data converted succesfully")
        f.close()
                



    
    




    
