import wx, dwGUI
"""Main script of calculation distance weight. """
import projectInitClass as pi
import os
import roxar
import multiprocessing, threading
import time
import subprocess as sp
projectPath = 'C:\PROJECTS\RMS\Emerald_10_PSJ.pro'
#projectPath = r'C:\PROJECTS\RMS\Emerald_10_Seis.pro' 
#projectPath = r'C:\PROJECTS\RMS\CALC_CUT_RMS10_Python.pro'
modulePath = r'D:\PythonRMSProjects\roxarAPI\DistanceWeight\\' #where script of parallel process is
tmpFilePath = modulePath + 'temp\\' #temporary directory
procCount = multiprocessing.cpu_count() # number of processors 
   
class DWFrame(dwGUI.Frame):
    def __init__(self, parent=None):
        self.fTitle = 'Distance Weight'
        dwGUI.Frame.__init__(self, parent, id=-1, title=self.fTitle, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX , name='MyFrame')
    
    def onRunClick(self, event):
        notFilled = ''
        self.paramCode = self.paramCodeEdt.GetValue().strip()
        self.distCell = self.distCellEdt.GetValue().strip()
        self.paramCodeEdt.SetValue(self.paramCode)
        self.distCellEdt.SetValue(self.distCell)
        if self.selGridLst.GetSelection() == wx.NOT_FOUND: notFilled += '-Select grid\n'
        if self.selParamLst.GetSelection() == wx.NOT_FOUND: notFilled += '-Select parameter\n'
        
        if self.paramCodeEdt.GetValue() == '': notFilled += '-Parameter code\n'
        if self.distCellEdt.GetValue() == '': notFilled += '-Distance cell\n'
        if notFilled.strip() != '': 
            notFilled = 'Fields:\n' + notFilled + 'should be filled out'
            dlg = wx.MessageDialog(None, notFilled, 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        elif not self.paramCodeEdt.GetValue().isdigit():
            dlg = wx.MessageDialog(None, "'Parameter code' should be positive integer", 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()    
        elif not self.distCellEdt.GetValue().isdigit():
            dlg = wx.MessageDialog(None, "'Distance cell' should be positive integer", 'Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            self.SetTitle(self.fTitle)
            self.runBtnEnable(False)
            task.cancelFlag = False
            t = threading.Thread(target=task.initCalc)
            t.start()
            frame.progress.SetValue(0)

    def onGridChoice(self, event):
        project.setGrid(event.GetString())
        self.selParamLst.Set(project.getProps())
        
    def onParamChoice(self, event):
        self.prop = event.GetString()
    
    def onSaveClick(self, event):
        #global project
        if not task.cancelFlag:
            project.save()
            
    def onCancelClick(self, event):
        task.cancelFlag = True
        for subProc in task.subProcs:
            subProc.terminate()
        
    def onCloseClick(self, event):
        self.Close(True)
    
    def onCloseWindow(self, event):
        if not task.isFinished:
            self.onCancelClick(event)
        project.close()
        self.Destroy()

class DWTask():
    def __init__(self):
        self.cancelFlag = False 
        self.subProcs = []
        self.paramCode = 0
        self.distCell = 0
        self.isFinished = True
        
    def mpCalcDistance(self):
        """
        divide total count of cells into parts and put information to list of jobs
        each process gets information from which cell it has to make calculation and how many cells it has to work
        """
        
        cellCountInJobInt = int(project.defined_cell_count/procCount)
        cellCountInJobRest = project.defined_cell_count%procCount
          
        firstCellInJob = 0
        for i in range(procCount):
            cellCountInJob = cellCountInJobInt
            if (cellCountInJobRest > 0):
                cellCountInJob += 1
                cellCountInJobRest -= 1
            self.jobs.append((firstCellInJob, cellCountInJob))
            firstCellInJob += cellCountInJob
                
        if not self.cancelFlag: 
            #start parallel processes
            self.subProcs =[]  
            for i in range(len(self.jobs)):
                subProc = sp.Popen('pythonw %sweightCalcProc.py %s %s %s %s %s' % (modulePath, self.jobs[i][0], self.jobs[i][1], tmpFilePath, self.paramCode, self.distCell), stdout = sp.PIPE)
                self.subProcs.append(subProc)
                
            thProgress = threading.Thread(target=self.updateProgress)
            thProgress.start()
     
            #wait until all processes finish
            for subProc in self.subProcs:
                subProc.wait()  

    def initCalc(self):
        """Upload and consolidate data"""
        startTime = time.time()
        lWeight = []
        self.jobs = []
        self.isFinished = False
        self.ch_prop_value = project.getPropValue(frame.prop)
        self.paramCode = frame.paramCode
        self.distCell = frame.distCell
                   
        pdist = project.createProp("PDistance")
        pdist.set_values(0)
        
        #create teporary directory
        if not os.path.exists(tmpFilePath):
            os.mkdir(tmpFilePath)
        
        #data uploading to external files in temporary directory
        f = open(tmpFilePath + 'ch_prop_value.txt', 'w')
        f.writelines([str(item) for item in self.ch_prop_value])
        f.close()
        f = open(tmpFilePath + 'cell_indices.txt', 'w')
        f.writelines(['%s %s %s\n' % (item[0], item[1], item[2]) for item in project.cell_indices]) # \n при записи в файл трансформируется в \r\n 
        f.close()
        
        self.mpCalcDistance()
         
        if not self.cancelFlag:        
            for i in range(len(self.jobs)):
                file = open('%sweight_%s.txt' % (tmpFilePath, self.jobs[i][0]), 'r')
                cells = file.read().split('\n')[:-1]
                lWeight = lWeight + [float(item) for item in cells]
                file.close()
            pdist.set_values(lWeight)
            
            frame.SetTitle('%s Execution time: %s' %(frame.fTitle, time.strftime("%X", time.gmtime(time.time() - startTime)) ))
            
        else: print('Terminated by user') 
        self.isFinished = True
        #frame.progress.SetValue(0)
        frame.runBtnEnable(True)
        self.removeFiles()
    
    def removeFiles(self):
        """remove temporary files and directory"""
        if os.path.exists(tmpFilePath):
            for item in os.listdir(path=tmpFilePath):
                isRemoved = False
                #waiting when process close files
                while not isRemoved:
                    try: 
                        os.remove(tmpFilePath + item)
                        isRemoved = True
                    except PermissionError:
                        pass
            os.rmdir(tmpFilePath) 
            
    def updateProgress(self):
        """
        Update the progress bar
        """
        while not os.path.exists('%sfifo.txt' % tmpFilePath): #waiting while file fifo will be exist
            time.sleep(0.5)    
        fifo = open('%sfifo.txt' % tmpFilePath, 'r')
        while not self.isFinished:
            
            line = fifo.readline()[:-1]
            if line.isdigit():
                prog = int(line) * procCount
                prog = int(prog * 50 / project.defined_cell_count)
                frame.progress.SetValue(prog)
               
        frame.progress.SetValue(50)
        fifo.close() 
               
if __name__ == '__main__':
    app = wx.App() 
    frame = DWFrame(parent=None)
    frame.Centre()
    
    project = pi.RMSProject(projectPath)
    task = DWTask()
    
    grids = project.getGrids()
    frame.selGridLst.Set(grids)
  
    
    frame.numProcBtn.SetLabel('CPU num.: %s' % str(procCount))
    frame.Show()
    app.MainLoop()
    
    
   # properties = grid_model.properties