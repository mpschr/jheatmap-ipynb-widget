from IPython.html import widgets
import uuid
from IPython.utils.traitlets import Unicode
from IPython.display import display, Javascript
import pandas
import os



# Define our JHeatmap and its target model and default view.
TMP = "tmp"


class JHeatmap(widgets.DOMWidget):
    _view_name = Unicode('JHeatmapWidget', sync=True)

    def __init__(self, values_df: pandas.DataFrame,
                 rows: list=[],
                 cols: list=[],
                 init_config: str="",
                 autodraw: bool=True,
                 *pargs,
                 **kwargs):
        """


        :type values_df: pandas.DataFrame
            :param values_df:
            :param rows:
            :param cols:
            :param init_config:
            :param autodraw:
            :param pargs:
            :param kwargs:
            """
        widgets.DOMWidget.__init__(self, *pargs, **kwargs)
        self._autodraw = autodraw
        self._js_loaded = False
        values_df = self._primary_col(cols, values_df)
        values_df = self._primary_row(rows, values_df)

        self._tmp_file_values = self._get_tmp_filename(".values")

        values_df.to_csv(self._tmp_file_values, quoting=None, sep="\t", index=False, header=True)
        self._init_config = init_config

        #print(values_df.columns)
        #print(self._tmp_file_values)

        if (autodraw):
            self._draw()

            #       def _ipython_display_(self, *pargs, **kwargs):

            #        # Show the widget, then send the current state
            #        widgets.DOMWidget._ipython_display_(self, *pargs, **kwargs)
            #        self.send({'key': 'values', 'action': 'init', 'value': self._values})
            #        self.send({'key': 'initData', 'action': 'init', 'value': self._initData})

    @staticmethod
    def _primary_row(rows, values_df) -> pandas.DataFrame:
        if len(rows) != 0:
            df_columns = list(values_df.columns)
            row_primary = rows[0]
            if len(rows) > 0 and df_columns.index(row_primary) != 1:
                old_order = df_columns[1:]
                new_order = df_columns[:1]
                new_order.append(row_primary)
                old_order.remove(row_primary)
                new_order += old_order
                values_df = values_df[new_order]
        return values_df

    @staticmethod
    def _primary_col(cols, values_df) -> pandas.DataFrame:
        if len(cols) != 0:
            df_columns = list(values_df.columns)
            col_primary = cols[0]
            if df_columns.index(col_primary) != 0:
                old_order = df_columns
                old_order.remove(col_primary)
                new_order = [col_primary] + old_order
                values_df = values_df[new_order]
        return values_df

    @staticmethod
    def _get_tmp_filename(filename):
        tmp_base = "jheatmap-" + str(uuid.uuid1())
        if not os.path.exists(TMP):
            os.mkdir(TMP)
        return TMP + "/" + tmp_base + filename


    def dummy_message(self):
        print("dummying")
        self.send({"action" : "dummy_message"})


    def redraw(self):
        self.send({
                     "action" : "draw",
                     "value" : "{data : { values : new jheatmap.readers.TableHeatmapReader( { url : '" + self._tmp_file_values + "'} ) }}"
                   })


    def _draw(self):

        if (self._js_loaded == False):
            self._js_loaded = True
            self._publish_js()
        self.redraw()


    def _publish_js(self):
        with open('./widget_jheatmap_loader.js', 'r') as f:
            display(Javascript(data=f.read()))

