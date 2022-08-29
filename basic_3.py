# Please install psutil first for recording the memory usage
# pip install psutil
import sys
from resource import *
import time
import psutil
# Hardcode deltaE and alphaPQ
deltaE = 30
alpha = {
    'A': {
        'A': 0,
        'C': 110,
        'G': 48,
        'T': 94
    },
    'C': {
        'A': 110,
        'C': 0,
        'G': 118,
        'T': 48
    },
    'G': {
        'A': 48,
        'C': 118,
        'G': 0,
        'T': 110
    },
    'T': {
        'A': 94,
        'C': 48,
        'G': 110,
        'T': 0
    },
}

# Input string generator
def InputGenerator(inputFilePath):
    f = open(inputFilePath)
    line = f.readline()
    str1 = line[0:len(line)-1]
    line = f.readline()
    generateSelector = 1
    while line:
        if(line[0] not in ['A', 'C', 'G', 'T']):
            if generateSelector == 1:
                str1 = str1[0:int(line)+1] + str1 + str1[int(line)+1:]
            else:
                str2 = str2[0:int(line)+1] + str2 + str2[int(line)+1:]
        else:
            str2 = line[0:len(line)-1]
            generateSelector = 2
        line = f.readline()
    f.close()
    return str1, str2


def OutputFileGenerator(outputFilePath, str1Sol, str2Sol, cost, timeUsage, memoryUsage):
    with open(outputFilePath, 'w') as f:
        f.write(str(cost)+'\n')
        f.write(str1Sol+'\n')
        f.write(str2Sol+'\n')
        f.write(str(timeUsage)+'\n')
        f.write(str(memoryUsage)+'\n')

# function for computing the cost and return the solution (basic)
def ComputeCostOfAlignment(str1, str2):
    # Initialize opt array
    m = len(str1)
    n = len(str2)
    opt = [[-1 for col in range(n+1)] for row in range(m+1)]
    for i in range(n+1):
        opt[0][i] = i * deltaE
    for i in range(m+1):
        opt[i][0] = i * deltaE

    # Fill opt (bottom_up)
    for j in range(1, n+1):
        for i in range(1, m+1):
            opt[i][j] = min(
                alpha[str1[i-1]][str2[j-1]] + opt[i-1][j-1],
                deltaE + opt[i-1][j],
                deltaE + opt[i][j-1]
            )

    # Find the optimal solution (top_down)
    i = m
    j = n
    solstr1 = ''
    solstr2 = ''
    while True:
        if (i == 0):
            solstr1 = ('_'*j) + solstr1
            solstr2 = str2[:j] + solstr2
            break
        if (j == 0):
            solstr2 = ('_'*i) + solstr2
            solstr1 = str1[:i] + solstr1
            break
        if opt[i][j] == alpha[str1[i-1]][str2[j-1]] + opt[i-1][j-1]:
            solstr1 = str1[i-1] + solstr1
            solstr2 = str2[j-1] + solstr2
            i = i-1
            j = j-1
        elif opt[i][j] == deltaE + opt[i][j-1]:
            solstr1 = '_' + solstr1
            solstr2 = str2[j-1] + solstr2
            j = j-1
        elif opt[i][j] == deltaE + opt[i-1][j]:
            solstr1 = str1[i-1] + solstr1
            solstr2 = '_' + solstr2
            i = i-1  
    # return solution and cost
    return solstr1, solstr2, opt[m][n]

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def main(argv):
    inputFilePath = argv[1]
    outputFilePath = argv[2]

    # Generate the strs
    str1, str2 = InputGenerator(inputFilePath)

    # Initialize measuring time amd memory usages
    t0 = 0
    timeUsage = 0
    memoryBefore = process_memory()
    t0 = time.time()

    # Compute the sol and cost
    str1Sol, str2Sol, cost = ComputeCostOfAlignment(str1, str2)

    # Record the usages
    timeUsage = ( time.time() - t0 ) * 1000
    memoryUsage = process_memory() - memoryBefore
    
    '''
    # Print results (For Test)
    print("InputSize:"+str(len(str1)+len(str2)))
    print("Cost: " + str(cost))
    print("Solution:")
    print(str1Sol)
    print(str2Sol)
    print("timeUsage: " + str(timeUsage) + " ms")
    print("memoryUsage: " + str(memoryUsage) + " KB")
    '''
    # Write output file
    OutputFileGenerator(outputFilePath, str1Sol, str2Sol,
                        cost, timeUsage, memoryUsage)


if __name__ == "__main__":
    main(sys.argv)
