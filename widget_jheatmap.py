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
                 autoshow: bool=True,
                 popup: bool=False,
                 *pargs,
                 **kwargs):
        """




        :type popup: bool
        :param popup:
        :type values_df: pandas.DataFrame
            :param values_df:
            :param rows:
            :param cols:
            :param init_config:
            :param autoshow:
            :param pargs:
            :param kwargs:
            """
        widgets.DOMWidget.__init__(self, *pargs, **kwargs)
        self._autoshow = autoshow
        self._js_loaded = False
        self._popup = None
        values_df = self._primary_col(cols, values_df)
        values_df = self._primary_row(rows, values_df)

        self._tmp_file_values = self._get_tmp_filename(".values")

        values_df.to_csv(self._tmp_file_values, quoting=None, sep="\t", index=False, header=True)
        self._init_config = init_config

        if popup:
            self._popup = widgets.PopupWidget()
            self._popup.description = "JHeatmap"
            self._popup.button_text = "Show heatmap"
            self._popup.children = [self]
            if autoshow:
                self._popup.on_displayed(self.show())
        else:
            if autoshow:
                display(self)
            #display(popup)

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


    def exec_js(self, js):

        self.send({
            "action": "exec",
            "value": js
        })


    def _ipython_display_(self, **kwargs):
        # Show the widget, then send the current state
        widgets.DOMWidget._ipython_display_(self, **kwargs)

        if not self._autoshow:
            return

        if not self._js_loaded:
            self._js_loaded = True
            self._publish_js()

        print("display!")

        init = "";
        funcs = " heatmap.options.container[0]._heatmapInstance = heatmap; "
        init += "init : function(heatmap) {" + funcs + "}"

        self.send({
            "action": "draw",
            "value": "{data : { values : new jheatmap.readers.TableHeatmapReader( { url : '" + self._tmp_file_values + "'} ) }, " + init + " }"
        })

    def show(self):
        self._autoshow = True
        if self._popup is None:
            self._ipython_display_()
        else:
            display(self._popup)
            self._ipython_display_()
            #display(self._popup.children[0])
            #self._draw()

    def redraw(self):
        print("re-drawing!")
        self._ipython_display_()



    @staticmethod
    def _publish_js():
        with open('./widget_jheatmap_loader.js', 'r') as f:
            display(Javascript(data=f.read()))

