from IPython.html import widgets # Widget definitions
from IPython.utils.traitlets import Unicode, CInt, CFloat # Import the base Widget class and the traitlets Unicode class.
from IPython.display import display, Javascript


# Define our JHeatmap and its target model and default view.
class JHeatmap(widgets.DOMWidget):
    _view_name = Unicode('JHeatmapView', sync=True)
    
    def __init__(self, values, rows = "", cols = "", initData = {}, *pargs, **kwargs):
        widgets.DOMWidget.__init__(self, *pargs, **kwargs)
        
        self._publish_js()

        self._initData = initData
        self._values = values
        #self._send_dict_changes(eventful_graph.graph, 'graph')
        #self._send_dict_changes(eventful_graph.node, 'node')
        #self._send_dict_changes(eventful_graph.adj, 'adj')

#    def _ipython_display_(self, *pargs, **kwargs):
        
#        # Show the widget, then send the current state
#        widgets.DOMWidget._ipython_display_(self, *pargs, **kwargs)
#        self.send({'key': 'values', 'action': 'init', 'value': self._values})
#        self.send({'key': 'initData', 'action': 'init', 'value': self._initData})

    def _publish_js(self):
        with open('./widget_jheatmap_kk.js', 'r') as f:
            display(Javascript(data=f.read()))

