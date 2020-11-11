
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
    
    for x, group_of_covariates in enumerate(covariates):
        print()
        print(expected_responses[x])
        for i, covariate in enumerate(group_of_covariates):
            if i % (width) == 0:
                print()
            print(covariate, end = '')

    return covariates, expected_responses

def SeperateDigids(covariates):     #covariates is single input, its list, not list of lists
    seperated_digid = []
    digid_indexes = []
   
   
    for x,covariate in enumerate(covariates):
        pass# to do her: check if covariate has '0' as neighbour. If has, append x to digid_indexes
            # mabe then 


if __name__ == '__main__':  
    ExtractSigns('data.txt', 20, 60)
    
