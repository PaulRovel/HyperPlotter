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
        
        self.Ax2d=hyperPlotter.plotfig.add_subplot()
        self.Ax3d=hyperPlotter.plotfig.add_subplot(projection='3d')
        self.Ax3d.set_visible(False)
        self.Ax:matplotlib.axes.Axes=self.Ax2d

        
        self.plotIndex=plotIndex
        self.MainImage=self.Ax.imshow(np.zeros((1,1)),extent=hyperPlotter.defaultExtent,cmap='seismic')
        self.Ax.set_xlabel('x')
        self.Ax.set_ylabel('y')
        self.Ax.set_title('Title')
        self.colorbar = plt.colorbar(mappable=self.MainImage,ax=self.Ax)
        self.scatters={}
        self.customPlottableData={}

        #Here : all state variables to memorize the state of the Plot
        self.state3D:bool=False
        self.stateMapPlottable:str=None
        self.stateScatterPlottable:set[str]=set()
        self.stateCustomPlottable:dict[str,list]={}
    
    def setNewMap(self,newMap:MapPlottable):
        self.MainImage.set(data=np.flip(newMap.data.T,axis=0))
        self.stateMapPlottable=newMap.label
        self.Ax.set_title(newMap.title)
        if newMap.symdata:
            self.MainImage.set_clim(vmin=-newMap.vmax,vmax=newMap.vmax)
            self.MainImage.set_cmap(symColorMap)
        else:
            self.MainImage.set_clim(vmin=np.min(np.nan_to_num(newMap.data)),vmax=np.max(np.nan_to_num(newMap.data)))
            self.MainImage.set_cmap('viridis')
        self.colorbar.set_label(newMap.cblabel)
    
    def switchScatter(self,scatter:ScatterPlottable):
        if self.state3D:
            return
        if scatter.label in self.stateScatterPlottable:
            self.Ax.collections.remove(self.scatters.pop(scatter.label)) #remove the scatter from the axis and from the scatter dict
            self.stateScatterPlottable.remove(scatter.label)
        else:
            self.stateScatterPlottable.add(scatter.label)
            self.scatters[scatter.label]=self.Ax.scatter(scatter.x,scatter.y,s=1,c='black')
            self.scatters[scatter.label].set_label(scatter.legend)
        self.Ax.legend()
            
