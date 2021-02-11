"""
Formulario de opciones de rtklib para jupyter
"""

__version__="0.0.1"

from .options_form import grid as formulario

def save_config(path='/proyecto/conf.cfg'):
    with open(path,'w') as f:
        for i in f.children:
            print('{} ={}'.format(i.description,i.value),file=f)
