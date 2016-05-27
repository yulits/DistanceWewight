import roxar
"""self.project initialisation. Set and get grid and parameters"""
import numpy as np

class RMSProject():
    def __init__(self, projectPath, readonly=False):
        self.proj = roxar.Project.open(projectPath, readonly)
    
    def setGrid(self, gridModel):
        self.grid_model = self.proj.grid_models[gridModel]
        self.grid = self.grid_model.get_grid()
        self.properties = self.grid_model.properties
        self.gi = self.grid.grid_indexer
        self.cell_numbers = self.gi.get_cell_numbers_in_range((0,0,0), self.gi.dimensions)
        self.cell_indices = self.gi.get_indices(self.cell_numbers)
        self.defined_cell_count = self.grid.defined_cell_count
    
    def getPropValue(self, prop):
        return self.properties[prop].get_values()
    
    def getGrids(self):
        return self.proj.grid_models.keys()
    
    def getProps(self):
        return self.properties.keys()
    
    def createProp(self, prop):
        return self.properties.create(prop, roxar.GridPropertyType.continuous, np.float32)
    
    def save(self):
        self.proj.save()
    
    def close(self):
        self.proj.close()
    
