from . import static
from ipywidgets import GridspecLayout,Text,FloatText,IntText
from itertools import product

def process(opt,key):
    if isinstance(opt,str):
        return Text(opt,description=key.replace('_','-'))
    if isinstance(opt,float):
        return FloatText(opt,description=key.replace('_','-'))
    if isinstance(opt,int):
        return IntText(opt,description=key.replace('_','-'))
    return opt

widgets = [process(static.__dict__[item],item) for item in static.__dict__ if not item.startswith("__")]

length = len(widgets) // 3 + 1

grid = GridspecLayout(length,3)

for i,j in product(range(length),range(3)):
    try:
        grid[i,j]= widgets[3*i+j]
    except IndexError:
        break
