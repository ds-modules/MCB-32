import qgrid
import pandas as pd
import numpy as np
from datascience import *

num_grids = 0

def create_table(num_rows, num_cols, names):
    global num_grids
    s = ",".join(names)
    for i in np.arange(num_rows):
        s += "\n" + "," * (num_cols - 1)
    with open("data/empty-grid-{}.csv".format(num_grids), "w+") as f:
              f.write(s)
    return None
        
def generate_grid(num_rows, num_cols, names, preset_values=None):
    global num_grids
    assert type(preset_values) == dict or preset_values == None, "preset_values must be a dict"
    create_table(num_rows, num_cols, names)
    df = pd.read_csv("data/empty-grid-{}.csv".format(num_grids), index_col=None)
    if preset_values:
        for key in preset_values.keys():
            df[key] = preset_values[key]
    num_grids += 1
    grid = qgrid.show_grid(df)
    return grid

def get_table(grid):
    return Table.from_df(grid.get_changed_df())