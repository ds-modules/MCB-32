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
        
def generate_grid(num_rows, num_cols, names):
    global num_grids
    create_table(num_rows, num_cols, names)
    df = pd.read_csv("data/empty-grid-{}.csv".format(num_grids))
    num_grids += 1
    grid = qgrid.show_grid(df)
    return grid

def get_table(grid):
    return Table.from_df(grid.get_changed_df())