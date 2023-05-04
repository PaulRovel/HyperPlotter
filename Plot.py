import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import matplotlib.axes
import mpl_toolkits.mplot3d.axes3d
import matplotlib.colorbar
from matplotlib import cm

from .Plottable import *

symColorMap = matplotlib.colormaps['Spectral_r']
symColorMap._segmentdata['blue'][5]=np.array([0.5,1.0,1.0])
symColorMap._segmentdata['blue'][6]=np.array([0.6,0.6,0.6])

class Plot():
    
    def __init__(self,hyperPlotter,plotIndex,xlabel='x',ylabel='y'):
        
        self.plotIndex=plotIndex
        self.extent=hyperPlotter.defaultExtent
        self.hyperPlotter = hyperPlotter

        self.Ax2d:matplotlib.axes.Axes=hyperPlotter.plotfig.add_subplot()
        self.Ax3d:mpl_toolkits.mplot3d.axes3d.Axes3D=hyperPlotter.plotfig.add_subplot(projection='3d')
        self.Ax3d.set_visible(False)
        self.Ax3d.autoscale(enable=True)
        self.Ax:matplotlib.axes.Axes=self.Ax2d
        
        self.MainImage=self.Ax2d.imshow(np.zeros((1,1)),extent=hyperPlotter.defaultExtent,cmap='seismic')
        X = np.linspace(self.extent[0], self.extent[1], 17*19) #This isn’t correct + make it correspond to core data!
        Y = np.linspace(self.extent[2], self.extent[3], 17*19)
        X, Y = np.meshgrid(X, Y)
        self.MainSurf = self.Ax3d.plot_surface(X,Y,np.zeros((17*19,17*19)),cmap='viridis')
        self.Ax3d.set_xlabel(xlabel)
        self.Ax3d.set_ylabel(ylabel)
        
        self.Ax2d.set_xlabel(xlabel)
        self.Ax2d.set_ylabel(ylabel)
        self.Ax2d.set_title('Title')
        self.colorbar:matplotlib.colorbar.Colorbar = plt.colorbar(mappable=self.MainImage,ax=self.Ax)
        self.colorbarData:list=[]
        self.Ax3d.set_position(self.Ax3d.get_position().translated(-0.1,0.))
        #self.Ax3d.set_position(self.Ax2d.get_position())

        #Here : all state variables to memorize the state of the Plot
        self.state3D:bool=False
        self.stateMapPlottable:str=None
        self.state3DMapPlottable:str=None
        self.stateScatterPlottable:dict[str,list]={}
        self.stateCustomPlottable:dict[str,list|dict]={}
    
    def setNewMap(self,newMap:MapPlottable):
        if self.state3D:
            self.state3DMapPlottable=newMap.label
            self.MainSurf.remove()
            X = np.linspace(self.extent[0], self.extent[1], newMap.data.shape[0]) #This isn’t correct + make it correspond to core data!
            Y = np.linspace(self.extent[2], self.extent[3], newMap.data.shape[1])
            X, Y = np.meshgrid(X, Y)
            if newMap.symdata:
                if newMap.vmax==None:
                    self.MainSurf = self.Ax3d.plot_surface(X,Y,newMap.data,cmap=symColorMap,vmin=-np.max(np.abs(np.nan_to_num(newMap.data))),vmax=np.max(np.abs(np.nan_to_num(newMap.data))))
                else:
                    self.MainSurf = self.Ax3d.plot_surface(X,Y,newMap.data,cmap=symColorMap,vmin=-newMap.vmax,vmax=newMap.vmax)
            else:
                self.MainSurf = self.Ax3d.plot_surface(X,Y,newMap.data,cmap='viridis',vmin=np.min(np.nan_to_num(newMap.data)),vmax=np.max(np.nan_to_num(newMap.data)))
            self.Ax3d.autoscale(enable=True)
            self.Ax3d.set_title(newMap.title)
        else:
            self.MainImage.set(data=np.flip(newMap.data.T,axis=0))
            self.stateMapPlottable=newMap.label
            self.Ax.set_title(newMap.title)
            if newMap.symdata:
                if newMap.vmax==None:
                    self.MainImage.set_clim(vmin=-np.max(np.abs(np.nan_to_num(newMap.data))),vmax=np.max(np.abs(np.nan_to_num(newMap.data))))
                else:
                    self.MainImage.set_clim(vmin=-newMap.vmax,vmax=newMap.vmax)
                self.MainImage.set_cmap(symColorMap)
            else:
                self.MainImage.set_clim(vmin=np.min(np.nan_to_num(newMap.data)),vmax=np.max(np.nan_to_num(newMap.data)))
                self.MainImage.set_cmap('viridis')
        self.refreshColorbar(currentMap=newMap)
        
    def refreshColorbar(self,currentMap=None):
        if self.state3D:
            self.colorbar.update_normal(self.MainSurf)
            if type(currentMap)==type(None):
                currentMap:MapPlottable=self.hyperPlotter.mapPlottables[self.state3DMapPlottable]
        else:
            self.colorbar.update_normal(self.MainImage)
            if type(currentMap)==type(None):
                currentMap:MapPlottable=self.hyperPlotter.mapPlottables[self.stateMapPlottable]
        self.colorbar.set_label(currentMap.cblabel)
        percents=[0,5,50,95,100]
        percentiles = np.nanpercentile(currentMap.data,percents)
        colors=['red','black','black','black','red']
        linewidths=[1,1,2,1,1]
        #self.colorbar.add_lines(levels=percentiles,colors=['red','black','black','black','red'],linewidths=[1,1,2,1,1])
        for item in self.colorbarData:
            item.remove()
        self.colorbarData=[]
        for i in range(5):
            self.colorbarData.append(self.colorbar.ax.axhline(y=percentiles[i],color=colors[i],linewidth=linewidths[i]))
            self.colorbarData.append(self.colorbar.ax.text(x=-.1,y=percentiles[i],s=str(percents[i]),horizontalalignment='right',verticalalignment='center',fontsize=8))
    

    def switchScatter(self,scatter:ScatterPlottable):
        if self.state3D:
            return
        if scatter.label in self.stateScatterPlottable:
            self.Ax.collections.remove(self.stateScatterPlottable.pop(scatter.label)) #remove the scatter from the axis and from the scatter dict
        else:
            self.stateScatterPlottable[scatter.label]=self.Ax.scatter(scatter.x,scatter.y,s=1,c='black')
            self.stateScatterPlottable[scatter.label].set_label(scatter.legend)
        self.Ax.legend()

    def updateDim(self):
        if self.state3D:
            self.Ax2d.set_visible(False)
            self.Ax3d.set_visible(True)
            self.Ax=self.Ax3d
        else:
            self.Ax2d.set_visible(True)
            self.Ax3d.set_visible(False)
            self.Ax=self.Ax2d
        self.refreshColorbar()
