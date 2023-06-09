import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import matplotlib
from matplotlib import cm

class MapPlottable():
    maxId = -1
    def __init__(self,data:np.ndarray,**kwargs):
        MapPlottable.maxId+=1
        self.data=data
        self.title= kwargs['title'] if 'title' in kwargs else 'Carte n°'+str(MapPlottable.maxId)
        self.label= kwargs['label'] if 'label' in kwargs else self.title
        self.cblabel= kwargs['cblabel'] if 'cblabel' in kwargs else ''
        self.symdata= kwargs['symdata'] if 'symdata' in kwargs else False
        self.vmax=kwargs['vmax'] if 'vmax' in kwargs else None

class ScatterPlottable():
    maxId = -1
    def __init__(self,x,y,**kwargs):
        ScatterPlottable.maxId+=1
        self.x=x
        self.y=y
        self.label= kwargs['label'] if 'label' in kwargs else 'Donnée n°'+str(ScatterPlottable.maxId)
        self.legend= kwargs['legend'] if 'legend' in kwargs else self.label

class CustomPlottable():
    maxId=-1
    def __init__(self,label='',type='button',onChangeFunc=lambda **args:None,refreshButton=None,activeIn='2d') -> None:
        if label=='':
            label='Fonction n°'+str(CustomPlottable.maxId)
        self.label=label
        self.type=type
        self.activeIn:str=activeIn
        CustomPlottable.maxId+=1
        self.onChangeFunc=onChangeFunc
        def standardRefreshButton(ax,**args):
            hyperPlt = args['hyperPlotter']
            match self.type:
                case 'button':
                    return pltwid.Button(ax=ax,label=self.label)
                case 'checkButton':
                    active = self.label in hyperPlt.currentPlot.stateCustomPlottable
                    return pltwid.CheckButtons(ax=ax,labels=[self.label],actives=[active])
        if refreshButton==None:
            refreshButton=standardRefreshButton
        self.refreshButtonFunc=refreshButton
    
    def isActive(self,is3D):
        if self.activeIn=='all':
            return True
        if self.activeIn=='2d':
            return not is3D
        if self.activeIn=='3d':
            return is3D

class CustomDisplayPlottable(CustomPlottable): #A Custom plottable that can display or hide stuff
    def __init__(self,label='',drawFunc=lambda **args:None,in3d=False):
        def onChangeFunc(**args):
            ax = args['ax']
            data = args['hyperPlotter'].currentPlot.stateCustomPlottable
            if self.label in data: #there is an entry for our name on the dict --» we need to erase its content
                for item in data[self.label]:
                    item.remove() #Erase the element that had been drawn
                del data[self.label] #delete the entry for our name
            else: #no entry --» create it
                data[self.label]=[]
                initialChildList = ax.get_children()
                drawFunc(ax=ax)
                newChildList = ax.get_children()
                for element in newChildList:
                    if element not in initialChildList:
                        data[self.label].append(element)
        if in3d:
            activein = '3d'
        else:
            activein = '2d'                    
        CustomPlottable.__init__(self,label=label,type='checkButton',onChangeFunc=onChangeFunc,activeIn=activein)

        
