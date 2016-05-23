# The global variable 'project' refers to the Project
# currently loaded in RMS. Script example:
#
# for well in project.wells:
#     print(well.name)

import numpy as np
import roxar 
import os
from datetime import datetime
import subprocess as sp


filePath = r'D:\PythonRMSProjects\roxarAPI\\DistanceWeight\\' #where script of parallel process is
tmpFilePath = filePath + 'temp\\' #temporary directory
procCount = 8 # how many processes will be start

def mpCalcDistance():
    #divide total count of cells into parts and put information to list of jobs
    #each process gets information from which cell it has to make calculation and how many cells it has to work
    cellCountInJobInt = int(defined_cell_count/procCount)
    cellCountInJobRest = defined_cell_count%procCount
        
    firstCellInJob = 0
    for i in range(procCount):
        cellCountInJob = cellCountInJobInt
        if (cellCountInJobRest > 0):
            cellCountInJob += 1
            cellCountInJobRest -= 1
        jobs.append((firstCellInJob, cellCountInJob))
        firstCellInJob += cellCountInJob
    
    #data uploading to external files in temporary directory
    f = open(tmpFilePath + 'ch_prop_value.txt', 'w')
    f.writelines([str(item) for item in ch_prop_value])
    f.close()
    f = open(tmpFilePath + 'cell_indices.txt', 'w')
    f.writelines(['%s %s %s\n' % (item[0], item[1], item[2]) for item in cell_indices]) # \n при записи в файл трансформируется в \r\n 
    f.close()
    
    #start parallel processes
    subProcs =[]  
    for i in range(len(jobs)):
        subProc = sp.Popen('pythonw %sweightCalcProc.py %s %s %s' % (filePath, jobs[i][0], jobs[i][1], tmpFilePath), stdout = sp.PIPE)
        subProcs.append(subProc)
    
    #wait until all processes finish
    for subProc in subProcs:
        subProc.wait()   
  
if __name__ == '__main__':
    startTime = datetime.now()
    #project = roxar.Project.open(r'C:\PROJECTS\RMS\CALC_CUT_RMS10_Python.pro', readonly = False)
    #grid_model = project.grid_models["Vol_2105ST_eoc2"]
    project = roxar.Project.open(r'C:\PROJECTS\RMS\Emerald_10_Seis.pro', readonly = False)
    grid_model = project.grid_models["Heterogeneity"]
    
    grid = grid_model.get_grid()
    properties = grid_model.properties
    #ch_prop = properties["Canales"]
    ch_prop = properties["channel"]
    ch_prop_value = ch_prop.get_values()

    pdist = properties.create("PDistance",
                    roxar.GridPropertyType.continuous,
                    np.float32)

    pdist_value = pdist.set_values(0)

    gi = grid.grid_indexer

    cell_numbers = gi.get_cell_numbers_in_range((0,0,0), gi.dimensions)
    cell_indices = gi.get_indices(cell_numbers)

    defined_cell_count = grid.defined_cell_count
    #create teporary directory
    if not os.path.exists(tmpFilePath):
        os.mkdir(tmpFilePath)
    
    lWeight = []
    jobs = []
    mpCalcDistance()
    
    for i in range(len(jobs)):
        file = open('%sweight_%s.txt' % (tmpFilePath, jobs[i][0]), 'r')
        cells = file.read().split('\n')[:-1]
        lWeight = lWeight + [float(item) for item in cells]
        file.close()
    pdist.set_values(lWeight)
    
    project.save()
    #remove temporary files and directory
    for item in os.listdir(path=tmpFilePath):
        os.remove(tmpFilePath + item)
    os.rmdir(tmpFilePath) 
    
    print(datetime.now() - startTime)
    print("Finished")
    

    
                                    
                    




