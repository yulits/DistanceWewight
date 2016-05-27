import os, sys
from math import sqrt

try: 
    startCell = int(sys.argv[1])
    countCell = int(sys.argv[2])
    filePath = sys.argv[3]
    paramCode = int(sys.argv[4])
    distCell = int(sys.argv[5])
except IndexError:
    startCell = 0
    countCell = 0
    filePath = os.curdir
    paramCode = 0
    distCell = 0
    
# def getLists():
#     # get data from files
#     global ch_prop_value 
#     file = open(filePath + 'ch_prop_value.txt', 'r')
#     ch_prop_value = [int(item) for item in list(file.read())]
#     
#     file = open(filePath + 'cell_indices.txt', 'r')
#     cells = file.read().split('\n')[:-1]
#     global cell_indices
#     cell_indices = []
#     global cell_coord_indices #create dictinary to define index by coordinates
#     cell_coord_indices = {}
#     index = 0
#     
#     for item in cells:
#         x = item.split()
#         cell_indices.append([int(x[0]), int(x[1]), int(x[2])])
#         cell_coord_indices['%s %s %s' % (x[0], x[1], x[2])] = index 
#         index += 1
    
def calcDistance():
    # calculate weight
    gauge = int(countCell/50)
    for ind in range(startCell, startCell+countCell):
        if ch_prop_value[ind] == paramCode:
            wt = 1.0
        else:
            max = 100
            cell_ind = cell_indices[ind]
            for i in range(-distCell, distCell):
                for j in range(-distCell, distCell):
                    if cell_ind[0]+i >=0 and cell_ind[1]+j >=0:
                        try:
                            index = cell_coord_indices['%s %s %s' % (cell_ind[0]+i, cell_ind[1]+j, cell_ind[2])]
                            if ch_prop_value[index] == paramCode:   
                                dist = sqrt(i**2 + j**2)
                                if dist < max:
                                    max = dist
                        except KeyError:
                            pass
                        
            wt = 1.0 - max/(distCell*sqrt(2))
            if wt > 1:
                wt = 1
            if wt < 0:
                wt = 0

        lWeight.append(wt)
        
        if startCell == 0 and ind % gauge == 0:
            fifo = open('%sfifo.txt' % filePath, 'a')
            fifo.write(str(ind) + '\n')
            fifo.close()
        
if __name__ == '__main__':
   
    # get data from files
    file = open(filePath + 'ch_prop_value.txt', 'r')
    ch_prop_value = [int(item) for item in list(file.read())]
    
    file = open(filePath + 'cell_indices.txt', 'r')
    cells = file.read().split('\n')[:-1]
    cell_indices = []
    cell_coord_indices = {}
    index = 0
    
    for item in cells:
        x = item.split()
        cell_indices.append([int(x[0]), int(x[1]), int(x[2])])
        cell_coord_indices['%s %s %s' % (x[0], x[1], x[2])] = index 
        index += 1
        
    lWeight = []
  
    calcDistance()
    
    
    
    f = open('%sweight_%s.txt' % (filePath, startCell), 'w')    
    f.writelines([str(item) + '\n' for item in lWeight])
    f.close()
        
