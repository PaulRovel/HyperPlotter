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
        self.vmax=kwargs['vmax'] if 'vmax' in kwargs else np.max(np.abs(np.nan_to_num(data)))

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
    def __init__(self,label='',type='button',onChangeFunc=lambda **args:None,refreshButton=None) -> None:
        if label=='':
            label='Fonction n°'+str(CustomPlottable.maxId)
        self.label=label
        self.type=type
        CustomPlottable.maxId+=1
        self.onChangeFunc=onChangeFunc
        def standardRefreshButton(ax,**args):
            match self.type:
                case 'button':
                    return pltwid.Button(ax=ax,label=self.label)
                case 'checkButton':
                    return pltwid.CheckButtons(ax=ax,labels=[self.label])
        if refreshButton==None:
            refreshButton=standardRefreshButton
        self.refreshButtonFunc=refreshButton

class CustomDisplayPlottable(CustomPlottable): #A Custom plottable that can display or hide stuff
    def __init__(self,label='',drawFunc=lambda **args:None):
        def onChangeFunc(**args):
            ax = args['ax']
            data = args['customPlottedData']
            if len(data): #there are elements on the list --» we need to erase
                while len(data):
                    data.pop().remove() #Erase the element that had been drawn
            else: #no elements on list --» create them
                initialChildList = ax.get_children()
                drawFunc(ax=ax)
                newChildList = ax.get_children()
                for element in newChildList:
                    if element not in initialChildList:
                        data.append(element)
                        
        CustomPlottable.__init__(self,label=label,type='checkButton',onChangeFunc=onChangeFunc)

        
