#! /usr/bin/env python

import wx

class Frame(wx.Frame):
    
    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name=''):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        #self.panel.SetBackgroundColour(wx.Colour(198, 226, 255))

        self.selGridLbl = wx.StaticText(self.panel, -1, 'Select grid')
        self.selGridLst = wx.Choice(self.panel, -1, size=(200,-1), choices = [])
        
        self.selParamLbl = wx.StaticText(self.panel, -1, "Select parameter")
        self.selParamLst = wx.Choice(self.panel, -1, size=(200,-1), choices = [])
        
        self.paramCodeLbl = wx.StaticText(self.panel, -1, "Parameter code")
        self.paramCodeEdt = wx.TextCtrl(self.panel, -1, "", size = (200, -1))
        
        self.distCellLbl = wx.StaticText(self.panel, -1, "Distance cell")
        self.distCellEdt = wx.TextCtrl(self.panel, -1, "", size = (200, -1))
        
        self.discripLbl = wx.StaticText(self.panel, -1, "Bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla")
        
        self.numProcBtn = wx.Button(self.panel, -1, label="N.Procs")
        self.numProcBtn.Enable(False)
        
        self.createdByLbl = wx.StaticText(self.panel, -1, "created by")
                                        
        self.helpBtn = wx.Button(self.panel, -1, label="Help")
        self.runBtn = wx.Button(self.panel, -1, label="Run")
        self.saveBtn = wx.Button(self.panel, -1, label="Save")
        self.cancelBtn = wx.Button(self.panel, -1, label="Cancel")
        self.closeBtn = wx.Button(self.panel, -1, label="Close")
        self.saveBtn.Enable(False)
        self.progress = wx.Gauge(self.panel, range=50, size=(-1, 22))
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.selSizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        self.selSizer.AddGrowableCol(1)
        self.selSizer.Add(self.selGridLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.selSizer.Add(self.selGridLst, 0, wx.EXPAND)
        self.selSizer.Add(self.selParamLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.selSizer.Add(self.selParamLst, 0, wx.EXPAND)
        self.selSizer.Add(self.paramCodeLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.selSizer.Add(self.paramCodeEdt, 0, wx.EXPAND)
        self.selSizer.Add(self.distCellLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        self.selSizer.Add(self.distCellEdt, 0, wx.EXPAND)
       
        self.mainSizer.Add(self.selSizer, 0, wx.EXPAND|wx.ALL, 10) 
        self.mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND|wx.ALL, 5)
        self.mainSizer.Add(self.discripLbl, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 10)
        self.mainSizer.Add((20,20), 1)
        
        self.infoSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.infoSizer.Add(self.numProcBtn)
        self.infoSizer.Add((20,20), 1)
        self.infoSizer.Add(self.createdByLbl)
        self.mainSizer.Add(self.infoSizer, 0, wx.EXPAND|wx.ALL, 10)
         
        self.mainSizer.Add(wx.StaticLine(self.panel), 0, wx.EXPAND|wx.ALL, 5)
        self.runSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.runSizer.Add(self.helpBtn)
        self.runSizer.Add((15,20), 1)
        self.runSizer.Add(self.runBtn)
        self.runSizer.Add((15,20), 1)
        self.runSizer.Add(self.saveBtn)
        self.runSizer.Add((15,20), 1)
        self.runSizer.Add(self.cancelBtn)
        self.runSizer.Add((15,20), 1)
        self.runSizer.Add(self.closeBtn)
        self.mainSizer.Add(self.runSizer, 0, wx.EXPAND|wx.ALL, 10)
        self.mainSizer.Add(self.progress, 0, wx.EXPAND|wx.ALL, 10)
        self.panel.SetSizer(self.mainSizer)
    
        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        self.mainSizer.Fit(self)
        self.mainSizer.SetSizeHints(self)
        
        self.Bind(wx.EVT_CHOICE, self.onGridChoice, self.selGridLst)
        self.Bind(wx.EVT_CHOICE, self.onParamChoice, self.selParamLst)
        self.Bind(wx.EVT_BUTTON, self.onRunClick, self.runBtn)
        self.Bind(wx.EVT_BUTTON, self.onHelpClick, self.helpBtn)
        self.Bind(wx.EVT_BUTTON, self.onSaveClick, self.saveBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancelClick, self.cancelBtn)
        self.Bind(wx.EVT_BUTTON, self.onCloseClick, self.closeBtn)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        
    def runBtnEnable(self, enable=True):
        self.runBtn.Enable(enable)
    
    def onGridChoice(self, event):
        pass
        
    def onParamChoice(self, event):
        pass
        
    def onRunClick(self, event):
        pass
    
    def onHelpClick(self, event):
        pass
    
    def onSaveClick(self, event):
        pass
    
    def onCancelClick(self, event):
        pass
        
    def onCloseClick(self, event):
        self.Close()
        
    def onCloseWindow(self, event):
        self.Destroy()
        
class App(wx.App):
    
    def OnInit(self):
        self.frame = Frame()
        self.frame.Center()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
if __name__ == '__main__':
    app = App() 
    app.MainLoop()
    
