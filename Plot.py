import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import matplotlib.axes
from matplotlib import cm
from .HyperPlotter import *

from .Plottable import *

symColorMap = matplotlib.colormaps['Spectral_r']
symColorMap._segmentdata['blue'][5]=np.array([0.5,1.0,1.0])
symColorMap._segmentdata['blue'][6]=np.array([0.6,0.6,0.6])

class Plot():
    
    def __init__(self,hyperPlotter,plotIndex):
        self.Ax2d:matplotlib.axes.Axes=hyperPlotter.plotfig.add_subplot()
        self.Ax3d=hyperPlotter.plotfig.add_subplot(projection='3d')
        self.Ax3d.set_visible(False)
        self.plotIndex=plotIndex
        self.MainImage=self.Ax2d.imshow(np.zeros((1,1)),extent=hyperPlotter.defaultExtent,cmap='seismic')
        self.Ax2d.set_xlabel('x')
        self.Ax2d.set_ylabel('y')
        self.Ax2d.set_title('Title')
        self.colorbar = plt.colorbar(mappable=self.MainImage,ax=self.Ax2d)
        self.scatters={}
        self.customPlottableData={}
    
    def setNewMap(self,newMap:MapPlottable):
        self.MainImage.set(data=np.flip(newMap.data.T,axis=0))
        self.Ax2d.set_title(newMap.title)
        if newMap.symdata:
            self.MainImage.set_clim(vmin=-newMap.vmax,vmax=newMap.vmax)
            self.MainImage.set_cmap(symColorMap)
        else:
            self.MainImage.set_clim(vmin=np.min(np.nan_to_num(newMap.data)),vmax=np.max(np.nan_to_num(newMap.data)))
            self.MainImage.set_cmap('viridis')
        self.colorbar.set_label(newMap.cblabel)
    
    def switchScatter(self,scatter:ScatterPlottable):
        if scatter.label in self.scatters:
            self.Ax2d.collections.remove(self.scatters.pop(scatter.label)) #remove the scatter from the axis and from the scatter dict
        else:
            self.scatters[scatter.label]=self.Ax2d.scatter(scatter.x,scatter.y)
            self.scatters[scatter.label].set_label(scatter.label)
        self.Ax2d.legend()
            
