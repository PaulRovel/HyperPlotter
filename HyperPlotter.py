import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
from matplotlib import cm

class HyperPlotter():
    def __init__(self):
        self.fig=plt.figure()
        gridSpec=self.fig.add_gridspec()
        self.menufig,self.plotfig=self.fig.subfigures(1,2,width_ratios=(3,7))
        self.axes=[] #Theses are the axes for plotting
        self.currentAxe=0
    
    def addAxes(self):
        self.axes.append(self.plotfig.add_subplot())

    def show(self):
        plt.show()
    
if __name__=='__main__':
    plotter = HyperPlotter()
    plotter.addAxes()
    plotter.axes[0].plot([1,2,3],[2,3,1])
    plotter.show()


