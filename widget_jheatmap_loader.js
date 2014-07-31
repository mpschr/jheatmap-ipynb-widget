require(["widgets/js/manager", "jheatmap/js/jheatmap-1.0.0.js", "widget_jheatmap.js"],
function(WidgetManager){
    // Register the widget with the widget manager.
    var widget = getJHeatmapWidgetInstance(WidgetManager);
    WidgetManager.register_widget_view('JHeatmapWidget', widget);
});