import pandas as pd
import ipywidgets as widgets
import numpy as np
from IPython.display import *
from datascience import *

# reference: https://link.jonathanferrari.com/table-widget.py

class Make:
    
    def headers(cols, labels):
        header_widgets = []
        for label in labels:
            label_lay = widgets.Layout(width="auto")
            header_label = widgets.HTML(f'<div class="table-cell"><b font-size:13px;>{label}</b></div>', layout = label_lay)
            header_lay = widgets.Layout(width="200px", margin="0 10px 10px 0")
            header_widget = widgets.VBox([header_label, widgets.HTML('<div style="height: 10px;"></div>')], layout = header_lay)
            header_widgets.append(header_widget)
        header_lay = widgets.Layout(grid_template_columns="repeat({0}, auto)".format(cols), 
                                    margin="0 0 10px", display="flex", flex_wrap="wrap", 
                                    justify_content="flex-start", border="none")
        headers = widgets.GridBox(header_widgets, layout = header_lay)
        return headers

    def grid(headers, cells):
        grid_items = [headers]
        for row_widgets in cells:
            row_lay = widgets.Layout(display = "flex", flex_wrap = "wrap", 
                                justify_content = "flex-start", border = "none")
            grid_item = widgets.GridBox(row_widgets, layout = row_lay)
            grid_items.append(grid_item)
        grid_lay = widgets.Layout(grid_template_rows = "auto", grid_gap = "0px", 
                                padding = "10px", border = "none", 
                                align_items = "flex-start")
        grid = widgets.GridBox(grid_items, layout = grid_lay)
        return grid

    def labels_and_types(cols, labels, types):
        if not labels:
            labels = [f"Column {i}" for i in range(cols)]
        if not types:
            types = "text"
        if isinstance(types, str):
            types = [types] * cols
        return labels, types

    def df(rows, labels, types, values):
        type_map = {"integer": 0, "decimal": 0.0, "text": ""}
        type_def = {"integer": np.dtype("int64"), "decimal": np.dtype("float64"), "text": np.dtype("object")}
        df = pd.DataFrame({label : [type_map[type]] * rows for label, type in zip(labels, types)})
        if values:
            for k, v in values.items():
                df[k] = pd.Series(v)
        df = df.astype({k: type_def[v] for k, v in zip(labels, types)})
        return df

    def cells(rows, cols, df):
        type_funcs = {np.dtype("int64"): lambda x: int(x), np.dtype("float64"): lambda x: float(x), np.dtype("object"): lambda x: str(x)}
        widget_types = {np.dtype("int64"): widgets.IntText, np.dtype("float64"): widgets.FloatText, np.dtype("object"): widgets.Text}
        cells = []
        for i in range(rows):
            row_widgets = []
            for j in range(cols):
                dtype = df.iloc[i, :].dtype
                func = type_funcs[dtype]
                val = func(df.iloc[i, j])
                cell_widget = widget_types[dtype]
                text_widget = cell_widget(value=val, 
                                           layout=widgets.Layout(width="200px", margin="0 10px 10px 0"))
                row_widgets.append(text_widget)
                # register callback to update dataframe when any cell value changes
                def update_df(change):
                    for ii in range(rows):
                        for jj in range(cols):
                            if cells[ii][jj] == change.owner:
                                df.iloc[ii, jj] = change.new
                text_widget.observe(update_df, names="value")
            cells.append(row_widgets)
        return cells

    def widget(grid):
        stylesheet = """
        <link rel="stylesheet" 
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" 
            integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+JQLM9vH+iA8tZIc5oTp75j7Bh/kzQ" 
            crossorigin="anonymous">

        <style>
            .table-cell { 
                display: table-cell; 
                padding: 10px 5px; 
                border-top: none !important; 
                border-right: none !important; 
                vertical-align: middle; 
            } 
            
            .form-control { 
                width: 80px; 
            }
        </style>
        """
        display(widgets.HTML(stylesheet))
        display(grid) 
    def table(rows, cols, labels = None, types = None, values = None):
    
        labels, types = Make.labels_and_types(cols, labels, types)
        
        # create empty dataframe with given number of rows and columns
        df = Make.df(rows, labels, types, values)

        # create table headers
        headers = Make.headers(cols, labels)
        
        # create table cells
        cells = Make.cells(rows, cols, df)
        # create a grid of widgets with headers and cells

        grid = Make.grid(headers, cells)

        # display the grid with Bootstrap styling
        Make.widget(grid)

        # return the dataframe
        return df
    
    def from_df(df):
        rows, cols = df.shape
        labels = df.columns.tolist()
        values = df.to_dict(orient="list")
        return Make.table(rows, cols, labels, values = values)

def get_table(df):
    for c in df.columns:
        try:
            df[c] = pd.to_numeric(df[c])
        except:
            continue
    return Table.from_df(df)
make_table = Make.table
from_df = Make.from_df
    
# Sample
# df = Make.table(5, 5,['id', 'age', 'height', "name", "weight"], ["integer", "integer", "decimal", "text", "decimal"])
