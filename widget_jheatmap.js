function getJHeatmapWidgetInstance(WidgetManager) {
    loadCSS();

    // Define the D3ForceDirectedGraphView
    var jHeatmapWidget = IPython.DOMWidgetView.extend({

		render: function(){

		    this.guid = 'jheatmap' + IPython.utils.uuid();
		    this.model.on('msg:custom', this.on_msg, this);
		    this.has_drawn = false;
            this.$el.text("Hello jHeatmap!");
            this.setElement($('<div/>', {id: this.guid}));
		    //this.custom_init();

		},

		custom_init: function() {
		    // Wait for element to be added to the DOM
            var that = this;
            setTimeout(function() {
                that.update();
            }, 0);
		},


		on_msg: function(message){

		    console.log("message received! : " + JSON.stringify(message));

		    var action = message.action;

		    if (action=='draw') {
		       this._inputData = message.value
		    }
		    this.update();
		},

		update: function(){
		    if (this._inputData == undefined) {
                         console.log("bad update!");
                         return;
            }
		    if (!this.has_drawn) {
			    this.has_drawn = true;
			    //var width = this.model.get('width'),
			    //var height = this.model.get('height');
                //this._inputData = eval("({data : { values : new jheatmap.readers.TableHeatmapReader( { url : 'data/genomic-alterations.tsv'} ) }})");

                var drawdiv = $("#" + this.guid);
                var options = eval("( " + this._inputData  + ")");
                drawdiv.heatmap(options);
		    }
		    return jHeatmapWidget.__super__.update.apply(this);
		},
	});

	return jHeatmapWidget;
}

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

