import xuiLoader
import wx

def loadXUI(fileName):
    hud = xuiLoader.XuiCanvas()
    hud.load(fileName)
    return hud
def saveXUI(fileName):
    hud.save(fileName)
#loop through hud.childElements and create a wx element for each one
#maybe try using separate windows for each group (xuiscene, advgroup, xuigroup, uistackpanel)
    



app = wx.App()
