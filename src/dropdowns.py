import ipywidgets as widgets

class Dropdown:
    
    def __init__(self, ops,desc):
        self._drop = widgets.Dropdown(
                            style={'description_width':'initial'},
                            options=ops,
                            value=ops[0],
                            description=desc,
                            disabled=False)
    
    def get(self):
        return self._drop
