import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import matplotlib
from matplotlib import cm

from .Plottable import *
from .Plot import *


class HyperPlotter():
    def __init__(self,defaultExtent=(0.,1.,0.,1)):
        self.defaultExtent=defaultExtent
        self.fig=plt.figure()
        self.menufig,self.plotfig=self.fig.subfigures(1,2,width_ratios=(3,7))
        self.mapPlottables:dict[str,MapPlottable]={}
        self.scatterPlottables:dict[str,ScatterPlottable]={}
        self.customPlottables:dict[str,CustomPlottable]={}
        self.plots:list[Plot]=[]
        self.currentPlot:Plot
        self.addPlot()

        #Create the Menu
        menucolor = 'lightgoldenrodyellow'
        self.mapSelectionAxe=self.menufig.add_axes([0.,.5,1.,.5],facecolor=menucolor)
        self.scatterSelectionAxe = self.menufig.add_axes([0.,0.,1.,.5],facecolor=menucolor)
        self.customSelectionAxes = []
        self.mapSelectionButton=None
        self.scatterSelectionButton=None

    
    def addPlot(self):
        self.plots.append(Plot(self,len(self.plots)))
        self.currentPlot=self.plots[-1]
    
    def addMapPlottable(self,newMap:MapPlottable):
        if newMap.label in self.mapPlottables:
            print('MapPlottable label already in use')
            raise KeyError
        self.mapPlottables[newMap.label]=newMap
    
    def addScatterPlottable(self,newScatter:ScatterPlottable):
        if newScatter.label in self.scatterPlottables:
            print('ScatterPlottable label already in use')
            raise KeyError
        self.scatterPlottables[newScatter.label]=newScatter
    
    def addCustomPlottable(self,custom:CustomPlottable):
        if custom.label in self.customPlottables:
            print('CustomPlottable label already in use')
            raise KeyError
        self.customPlottables[custom.label]=custom
    
    def addPlottable(self,plottables):
        if not hasattr(plottables,'__iter__'):
            plottables = [plottables]
        for plottable in plottables:
            if isinstance(plottable,MapPlottable):
                self.addMapPlottable(plottable)
            elif isinstance(plottable,ScatterPlottable):
                self.addScatterPlottable(plottable)
            elif isinstance(plottable,CustomPlottable):
                self.addCustomPlottable(plottable)
            else:
                print(plottable, 'does not seem to be plottable')
                raise TypeError
    

    
    def refreshMenu(self):
        self.mapSelectionAxe.remove()
        self.scatterSelectionAxe.remove()
        for ax in self.customSelectionAxes:
            ax.remove()
        self.customSelectionAxes=[]
        self.customSelectionButtons=[]

        totalLinesNumber=len(self.mapPlottables)+len(self.scatterPlottables)+len(self.customPlottables)+3 #3 Titles to add...
        linewidth=1/totalLinesNumber

        menucolor = 'lightgoldenrodyellow'

        selectionWidth = linewidth*len(self.mapPlottables)
        bottom = 1 - linewidth - selectionWidth
        self.mapSelectionAxe = self.menufig.add_axes([0.,bottom,1.,selectionWidth],facecolor=menucolor)
        self.mapSelectionAxe.set_title('Cartes :')
        labels = [label for label in self.mapPlottables]
        if len(labels):
            self.mapSelectionButton = pltwid.RadioButtons(ax=self.mapSelectionAxe,labels=labels)
        else :
            self.mapSelectionButton = None

        def mapButtonClick(label):
            if label in self.mapPlottables:
                self.currentPlot.setNewMap(self.mapPlottables[label])
                self.fig.canvas.draw()
        try:
            self.mapSelectionButton.on_clicked(mapButtonClick)
        except:
            pass

        selectionWidth = linewidth*len(self.scatterPlottables)
        bottom += - linewidth - selectionWidth
        self.scatterSelectionAxe = self.menufig.add_axes([0.,bottom,1.,selectionWidth],facecolor=menucolor)
        self.scatterSelectionAxe.set_title('Données :')
        labels = [label for label in self.scatterPlottables]
        if len(labels):
            self.scatterSelectionButton= pltwid.CheckButtons(ax=self.scatterSelectionAxe,labels=labels)
        else:
            self.scatterSelectionButton=None
        def scatterButtonClick(label):
            if label in self.scatterPlottables:
                self.currentPlot.switchScatter(self.scatterPlottables[label])
                self.fig.canvas.draw()

        try:
            self.scatterSelectionButton.on_clicked(scatterButtonClick)
        except:
            pass

        for custom in self.customPlottables.values():
            selectionWidth = linewidth
            bottom += -linewidth
            ax = self.menufig.add_axes([0.,bottom,1.,selectionWidth],facecolor=menucolor)
            button = custom.refreshButtonFunc(ax=ax)#TODO : HERE add all intersting context !
            if custom.label not in self.currentPlot.customPlottableData:
                self.currentPlot.customPlottableData[custom.label]=[]
            def redirectToOnChangeFunc(data,custom=custom): 
                #Here the custom=custom is to force function closure to de-reference the custom value here (before the next loop iteration)
                #Note that self is put in the closure after but it doesn’t matter much
                custom.onChangeFunc(customPlottedData=self.currentPlot.customPlottableData[custom.label],ax=self.currentPlot.Ax2d,data=data) # TODO : Here add all relevant data
                self.fig.canvas.draw()

            match custom.type:
                case 'button' | 'checkButton':
                    button.on_clicked(redirectToOnChangeFunc)
            self.customSelectionAxes.append(ax)
            self.customSelectionButtons.append(button) 
    

        
        
        


    def show(self):
        plt.show()


if __name__=='__main__':
    plotter = HyperPlotter()
    #plotter.addMapPlottable(MapPlottable(np.eye(10),title='test1'))
    #plotter.addMapPlottable(MapPlottable(np.linspace(-50,50,num=100).reshape((10,10)),title='test2',symdata=True))
    plotter.addScatterPlottable(ScatterPlottable([0,1,2,3],[3,2,1,0]))
    def draw(ax):
        ax.plot([0,1],[0,1])
        ax.text(0.5,0.5,'Hello it’s me !')
        ax.annotate('Un autre test des familles',xy=(1,1))
    plotter.addCustomPlottable(CustomDisplayPlottable(drawFunc=draw))
    plotter.refreshMenu()
    plotter.show()


