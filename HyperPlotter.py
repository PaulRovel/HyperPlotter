import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import matplotlib
from matplotlib import cm



class HyperPlotter():
    def __init__(self,defaultExtent=(0.,1.,0.,1)):
        self.defaultExtent=defaultExtent
        self.fig=plt.figure()
        self.menufig,self.plotfig=self.fig.subfigures(1,2,width_ratios=(3,7))
        self.mapPlottables:list[MapPlottable]=[]
        self.plots:list[Plot]=[]
        self.currentPlot:Plot
        self.addPlot()

        #Create the Menu
        menucolor = 'lightgoldenrodyellow'
        self.mapSelectionAxe=self.menufig.add_axes([0.,.5,1.,.5],facecolor=menucolor)
        self.mapSelectionButton=pltwid.RadioButtons(ax=self.mapSelectionAxe,labels=['Empty'])

    
    def addPlot(self):
        self.plots.append(Plot(self.plotfig,len(self.plots)))
        self.currentPlot=self.plots[-1]
    
    def addMapPlottable(self,newMaps):
        try:
            self.mapPlottables.extend(newMaps)
        except:
            self.mapPlottables.append(newMaps)
    
    def refreshMenu(self):
        pass

    def show(self):
        plt.show()

class Plot():
    def __init__(self,hyperPlotter:HyperPlotter,plotIndex):
        self.Ax2d=hyperPlotter.plotfig.add_subplot()
        self.Ax3d=hyperPlotter.plotfig.add_subplot(projection='3d')
        self.Ax3d.set_visible(False)
        self.plotIndex=plotIndex
        self.MainImage=self.Ax2d.imshow(np.zeros,extent=hyperPlotter.defaultExtent)
        self.Ax2d.set_xlabel('x')
        self.Ax2d.set_ylabel('y')
        self.Ax2d.set_title('Title')


class MapPlottable():
    def __init__(self,data:np.ndarray,**kwargs):
        self.data=data
        self.title= kwargs['title'] if 'title' in kwargs else 'Carte'
        self.label= kwargs['label'] if 'label' in kwargs else self.title
        self.cblabel= kwargs['cblabel'] if 'cblabel' in kwargs else ''
        self.symdata= kwargs['symdata'] if 'symdata' in kwargs else False
        self.vmax=kwargs['vmax'] if 'vmax' in kwargs else np.max(np.abs(np.nan_to_num(data)))

if __name__=='__main__':
    plotter = HyperPlotter()
    plotter.addPlot()
    plotter.currentPlot.Ax2d.plot([1,2,3],[2,3,1])
    plotter.show()


