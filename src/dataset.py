def readData(fileID):
    fileID = '../data/rand' + f'{fileID:04d}' + '.txt'
    file = open(fileID, 'r')
    temp = file.readline()
    temp = [int(i) for i in temp.strip().split()]
    data = {'numTasks': temp[0], 'numProcs': temp[1]}
    for i in file.readlines():
        i = [int(j) for j in i.strip().split()]
        tempStr = 'proc' + f'{i[0]:02d}'  # proc01, proc02, proc03,...
        data[tempStr] = {}
        data[tempStr]['procID'] = i[0]
        data[tempStr]['height'] = i[1]
        data[tempStr]['procTime'] = i[2]
        data[tempStr]['numPre'] = i[3]
        if i[3] > 0:
            for j in range(4, len(i)):
                tempStr2 = 'pre' + str(j - 3)  # pre1, pre2, pre3,...
                data[tempStr][tempStr2] = i[j]
    return data  # returns a dictionary
