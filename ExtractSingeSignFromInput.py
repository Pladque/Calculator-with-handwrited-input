import numpy as np
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
    
    
    '''for x, group_of_covariates in enumerate(covariates):
        print()
        print(expected_responses[x])
        for i, covariate in enumerate(group_of_covariates):
            if i % (width) == 0:
                print()
            print(covariate, end = '')'''

    return covariates, expected_responses

def findNeighbors(arr, ind, connected_ones, width):        #return indexes or digit
    #connected_ones is an array
    connected_ones.append(ind)
    try:
        if arr[ind + width] == 1 and ind + width not in connected_ones:           #checking below
            connected_ones.append(ind+ width)
            connected_ones += findNeighbors(arr, ind + width, connected_ones,width)
    except: pass

    try:
        if ind - width > 0 and arr[ind - width] == 1 and ind - width not in connected_ones:           #checking above
            connected_ones.append(ind - width)
            connected_ones += findNeighbors(arr, ind - width, connected_ones,width)
    except: pass

    try:
        if arr[ind+ width - 1] == 1 and ind + width - 1 not in connected_ones and ind % width != 0:       # checking below on diagnal left
            connected_ones.append(ind + width - 1)
            connected_ones += findNeighbors(arr, ind + width - 1, connected_ones,width)
    except: pass

    try:
        if arr[ind+ width + 1] == 1 and ind+ width + 1 not in connected_ones and (ind + 1) % width != 0:        # checking below on diagnal right
            connected_ones.append(ind + width + 1)
            connected_ones += findNeighbors(arr, ind + width + 1, connected_ones,width)
    except: pass

    try:
        if arr[ind - 1] == 1 and ind - 1 not in connected_ones and ind % width != 0:          # checking left
            connected_ones.append(ind - 1)
            connected_ones += findNeighbors(arr, ind - 1, connected_ones,width)
    except: pass

    try:
        if arr[ind + 1] == 1 and ind + 1 not in connected_ones and (ind + 1) % width != 0:          # checking right
            connected_ones.append(ind + 1)
            connected_ones += findNeighbors(arr, ind + 1, connected_ones,width)
    except: pass

    try:
        if ind - width - 1 >= 0 and arr[ind - width - 1] == 1 and ind - width - 1 not in connected_ones and ind % width != 0:          # checking up left
            connected_ones.append(ind - width - 1)
            connected_ones += findNeighbors(arr, ind - width - 1, connected_ones,width)
    except: pass

    try:
        if ind - width + 1 >= 0 and arr[ind - width + 1] == 1 and ind - width + 1 not in connected_ones and (ind + 1) % width != 0:          # checking up right
            connected_ones.append(ind - width + 1)
            connected_ones += findNeighbors(arr, ind - width + 1, connected_ones,width)
    except: pass

    return list(dict.fromkeys(connected_ones))
        
def SeperateDigids(covariates, width):     #covariates is single input, its list, not list of lists

    seperated_digids = [[],[],[]]
    digid_indexes = [[],[],[]]
    
    sign_ind = 0
    neighbors = []
    for x,covariate in enumerate(covariates):
        if covariate == 1 and x not in seperated_digids[0] and x not in seperated_digids[1] and x not in seperated_digids[2] and x < 750:   #x<750 is temp fix
            seperated_digids[sign_ind] = findNeighbors(covariates, x, [], width)
            sign_ind += 1

    return seperated_digids

def fillEmptySpaceInSeperatedDigits(sign, width = 1, expected_height = 0):      # to make all inputs be same size
    try:
        output_arr_size = max(sign) - min(sign)+ ( (max(sign) - min(sign))% width)
        filled_sign_arr = []

        for _ in range(min(sign)%width):
            filled_sign_arr.append(0)
        for _ in range(output_arr_size):
            if _ + min(sign) in sign:
                filled_sign_arr.append(1)
            else: filled_sign_arr.append(0)

        while len(filled_sign_arr) % width != 0:
            filled_sign_arr.append(0)

        while len(filled_sign_arr) < expected_height * width:
            filled_sign_arr.append(0)



        return filled_sign_arr
    except : pass
    return []

if __name__ == '__main__':
    covariates, responses = ExtractSigns('data.txt', 20, 60)

    seperated_digids = [[]]
    for x, group_of_covariates in enumerate(covariates):

        # converting form chars to ints
        for y, covariate in enumerate(group_of_covariates):
            if covariate == '0': group_of_covariates[y] = 0
            else: group_of_covariates[y] = 1

        for digid in SeperateDigids(group_of_covariates, 20):
            seperated_digids[x].append(fillEmptySpaceInSeperatedDigits(digid, width = 20, expected_height = 15))
            seperated_digids.append([])

    print(seperated_digids[0])

    for digids in seperated_digids[0]:
        for index, digid in enumerate(digids):
            if index % 20 == 0:
                print()
            print(digid, end = '')
        print()




    
