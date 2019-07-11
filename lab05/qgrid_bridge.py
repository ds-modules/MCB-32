import qgrid
import pandas as pd
import numpy as np
from datascience import *
from io import StringIO

def create_table(num_rows, num_cols, names):
    empty_csv = ",".join(names)
    for _ in range(num_rows):
        empty_csv += "\n" + "," * (num_cols - 1)
    return empty_csv
        
def generate_grid(num_rows, num_cols, names, preset_values=None):
    assert type(preset_values) == dict or preset_values == None, "preset_values must be a dict"
    empty_csv = create_table(num_rows, num_cols, names)
    df = pd.read_csv(StringIO(empty_csv), index_col=False)
    if preset_values:
        for key in preset_values.keys():
            df[key] = preset_values[key]
    grid = qgrid.show_grid(df)
    return grid

def get_table(grid):
    return Table.from_df(grid.get_changed_df())