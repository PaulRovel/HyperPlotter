import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
from matplotlib import cm

class HyperPlotter():
    def __init__(self):
        self.fig=plt.figure()
        gridSpec=self.fig.add_gridspec()
        self.menufig,self.plotfig=self.fig.subfigures(1,2,width_ratios=(3,7))
        self.plots=[]
        
        self.currentPlot:Plot
    
    def addPlot(self):
        self.plots.append(Plot(self.plotfig,len(self.plots)))
        self.currentPlot=self.plots[-1]

    def show(self):
        plt.show()

class Plot():
    def __init__(self,figure,plotIndex):
        self.Ax2d=figure.add_subplot()
        self.Ax3d=figure.add_subplot(projection='3d')
        self.Ax3d.set_visible(False)
        self.plotIndex=plotIndex

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


