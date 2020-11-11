
def ExtractSigns(file_name, width, height):
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if i % (height + 2) == 0:
                expected_response = line.split(';')
                expected_response[-1] = expected_response[-1].replace('\n', '')
                print(expected_response)


        f.close() 
if __name__ == '__main__':  
    ExtractSigns('data.txt', 20, 60)
    
