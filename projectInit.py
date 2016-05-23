import roxar
"""Project initialisation. Set and get grid and parameters"""
import numpy as np

def projectOpen(projectPath, readonly=False): 
    return roxar.Project.open(projectPath, readonly)
    
def setGrid(proj, gridModel):
    grid_model = proj.grid_models[gridModel]
    grid = grid_model.get_grid()
    global properties, cell_indices, defined_cell_count
    properties = grid_model.properties
    gi = grid.grid_indexer
    cell_numbers = gi.get_cell_numbers_in_range((0,0,0), gi.dimensions)
    cell_indices = gi.get_indices(cell_numbers)
    defined_cell_count = grid.defined_cell_count

def getPropValue(property):
    global properties
    return properties[property].get_values()

def getGrids(proj):
    return proj.grid_models.keys()

def getProps():
    global properties
    return properties.keys()

def createProp(property):
    global properties
    return properties.create(property, roxar.GridPropertyType.continuous, np.float32)

def projectSave(proj):
    proj.save()
    
def projectClose(proj):
    proj.close()
