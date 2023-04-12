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
        
        self.currentPlot=None
    
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

if __name__=='__main__':
    plotter = HyperPlotter()
    plotter.addPlot()
    plotter.currentPlot.Ax2d.plot([1,2,3],[2,3,1])
    plotter.show()


