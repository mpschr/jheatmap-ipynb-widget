require(["widgets/js/manager", "jheatmap/js/jheatmap-1.0.0.js"], function(WidgetManager, heatmap){
    loadCSS();
    // Define the D3ForceDirectedGraphView
    var JHeatmapView = IPython.DOMWidgetView.extend({

		render: function(){
                    

                    this.$el.text("Hello jHeatmap!"); 
		    this.guid = 'jheatmap' + IPython.utils.uuid();
		    this.setElement($('<div />', {id: this.guid}));
		    this.model.on('msg:custom', this.on_msg, this);
		    this.has_drawn = false;

		    // Wait for element to be added to the DOM
		    var that = this;
		    setTimeout(function() {
			that.update();
		    }, 0);
		},


		on_msg: function(content){
		    
		    var action = content.action;
		    var key = content.key;

		    if (action=='init') {
		       if (key == 'values') {
		       } else if (key == 'initData'){
			  this._inputData = content.value
		       }
		    }
		    this.update();
		},

		update: function(){
		    if (this._inputData == 'undefined' || this._values == 'undefined') {
                         alert("bad update!");
                         return;
                    }
		    if (!this.has_drawn) {
			this.has_drawn = true;
			var width = this.model.get('width'),
			    height = this.model.get('height');
			
			var drawdiv = $("#" + this.guid);
			//drawdiv.heatmap(this._inputData);
			drawdiv.heatmap({data : { values : new jheatmap.readers.TableHeatmapReader({ url : "quickstart-data.tsv"}) }});
		    }
		    return JHeatmapView.__super__.update.apply(this);
		},
	});

    
    // Register the D3ForceDirectedGraphView with the widget manager.
    WidgetManager.register_widget_view('JHeatmapView', JHeatmapView);
});

function loadCSS() {
	var $ = document; // shortcut
	var cssId = 'myCss';  // you could encode the css path itself to generate id..
	if (!$.getElementById(cssId))
	{
	    var head  = $.getElementsByTagName('head')[0];
	    var link  = $.createElement('link');
	    link.id   = cssId;
	    link.rel  = 'stylesheet';
	    link.type = 'text/css';
	    link.href = 'jheatmap/css/jheatmap-1.0.0.css';
	    link.media = 'all';
	    head.appendChild(link);
	}
}

