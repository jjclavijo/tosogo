from . import static
from ipywidgets import GridspecLayout, Text, FloatText, IntText
from itertools import product
import numbers

"""
NOTICE:

    There is intensive usage of globals inside here,
    this looks ugly, must refactor in the future.

    This may cause trouble if the same notebook handles more than one
    configuration file
"""


def process(opt, key):
    if isinstance(opt, str):
        return Text(opt, description=key.replace("_", "-"))
    if isinstance(opt, float):
        return FloatText(opt, description=key.replace("_", "-"))
    if isinstance(opt, int):
        return IntText(opt, description=key.replace("_", "-"))
    return opt


def new_form():
    # Create widget list
    widgets = [
        process(static.__dict__[item], item)
        for item in static.__dict__
        if not item.startswith("__")
    ]

    length = len(widgets) // 3 + 1

    # create grid
    grid = GridspecLayout(length, 3)

    # register widgets in grid.
    for i, j in product(range(length), range(3)):
        try:
            grid[i, j] = widgets[3 * i + j]
        except IndexError:
            break

    return grid


def load_conf(file, formulario):
    try:
        with open(file, "r") as f:
            confs = {
                i.strip(): j.strip() for i, j in [k.split("=") for k in f.readlines()]
            }
            # traverse the grid updating its children according to conf.
            for i in formulario.children:
                try:
                    if i.description == "pos1-navsys":
                        continue

                    opts = [j.split(":")[1] for j in i.options]
                    optsn = [j.split(":")[0] for j in i.options]

                    if (val := confs[i.description]) in opts:
                        i.value = i.options[opts.index(val)]
                    elif (val := confs[i.description]) in optsn:
                        i.value = i.options[optsn.index(val)]
                except AttributeError:
                    if isinstance(i.value, int):
                        if confs[i.description] == "":
                            i.value = -1
                        else:
                            i.value = int(confs[i.description])
                    elif isinstance(i.value, str):
                        i.value = confs[i.description]
                    elif isinstance(i.value, float):
                        i.value = float(confs[i.description])
                        if confs[i.description] == "":
                            i.value = -1
    except FileNotFoundError:
        pass


def save_conf(file, formulario):
    with open(file, "w") as f:
        # Traverse the grid, collecting each option.
        for i in formulario.children:
            try:
                if isinstance(i.value, (list, tuple)):
                    value = sum(
                        [int(v.split(":")[0]) for v in i.value if v.split(":")[0] != ""]
                    )
                else:
                    value = i.value.split(":")[-1]

                try:
                    if int(value) < 0:  # -1 is blank
                        value = ""
                except ValueError:
                    pass

            except AttributeError:
                value = i.value
                try:
                    if int(value) < 0:  # -1 is blank
                        value = ""
                except ValueError:
                    pass

            print("{} ={}".format(i.description, value), file=f)
