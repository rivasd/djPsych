
/**
 * A widget for allowing users to generate sets of our stimuli while controlling the properties through a GUI
 * 
 * @param	{jQuery.fn}	target			a jQuery selection of the the element that will hold this widget
 * @param {String[]}	microcomponents	An array of the names of all the available microcomponents on the server
 * @author Daniel Rivas
 * @date 2016-04-27
 */
function StimUI(target, microcomponents){
	var core={};
	var backend = {};
	var diagnostic;
	
	var cells;
	var table;
	var controller = new Array(2);
	
	var ui = $("<div>", {id:"generator-ui"});
	
	
	/**
	 * 
	 * 
	 */
	function handleDrop(evt){
		var movedImg = $("#"+evt.dataTransfer.getData('text'));
		var oldCoord = getCoord(movedImg);	
		movedImg.detach();
		$(this).append(movedImg);
		var newCoord = getCoord(movedImg);
		//TODO: finish this!
		
	}
	
	/**
	 * Event handler called on the element that is just starting to get dragged, sets up the data to be transferred,
	 * here the src attribute of our micro-component image
	 */
	function initDrag(evt){
		evt.dataTransfer.dropEffect = 'move';
		evt.dataTransfer.setData("text/plain", this.id);
	}
	
	
	/**
	 * Find the coordinates (row, column) of the cell that contains the given image
	 * @param	{jQuery}	img	a jQuery selection of the image whose coordinates we want
	 * @return 	{Array}
	 */
	function getCoord(img){
		var parent = img.parent('td');
		return parent.data('index');
	}
	
	/**
	 * Use this to load the microcomponents into memory so that they are ready to draw and launch the callback only after that
	 * @param {Function} callback	function to be run after all microcomponents are guaranteed to be loaded into Image objects 
	 */
	function loadImages(callback){
		//TODO: integrate with the general solution for user-uploaded content when we get to it
		var nbrOfImg = microcomponents.length
		var loadedSoFar = 0;
		
		function check(){
			loadedSoFar++;
			if(loadedSoFar === nbrOfImg){
				callback();
			}
		}
		
		microcomponents.forEach(function(elt, i, array) {
			var img = new Image();
			img.onload = check;
			img.src = '/static/djexperiments/simcat/attributes/'+elt;
			backend[elt] = img;
		});
	}
	
	/**
	 * Generates a table cell with all the UI needed to make it represent a settable micro-components
	 * @private
	 */
	function createCell(row, col){
		var $cell = $("<td></td>", {class:'stimUI-cell'});
		$cell.data('index', [row,col]);
		
		var mc = $("<img>", {id: 'microcomp-'+row+'-'+col, class: 'stimUI-thumbnail'});
		
		mc.attr('width', 36);
		mc.attr('height', 36);
		mc[0].src = '/static/djexperiments/simcat/attributes/Alpha.png';
		
		var selector = $("<select></select>");
		$cell.append(mc).append(selector);
		
		microcomponents.forEach(function(elt, i, array) {
			var option = $("<option>", {label: elt, value: '/static/djexperiments/simcat/attributes/'+elt});
			selector.append(option);
		});
		selector.on("change", function(e){
			mc[0].src = this.value;
		});
		return $cell;
	}
	
	/**
	 * Selects all td elements that make up the requested column in the table
	 * @private
	 * @param 	{number} 	idx		the 0-based index of the column to select
	 * @return	{jQuery.fn}			a jQuery selection of the td elements that make up the column
	 */
	function selectColumn(idx){
		return $("#stimUI-table td").filter(function(idx, elm){
			return $(elm).data('index')[1] === idx;
		});
	}
	
	
	/**
	 * Creates the table element that will hold our microcomponents and holds it in memory. DOES NOT insert it in the DOM 
	 */
	core.build = function(len){
		table = $("<table></table>", {id:'stimUI-table'});
		for(var i=0;i<3;i++){
			var row = $("<tr></tr>");
			var contRow = []
			for(var j=0;j<len;j++){
				
				var cell;
				if(i<2){
					cell = createCell(i, j);
					contRow.push(cell);
				}
				else{
					cell = $("<td></td>", {'class': 'stimUI-invariant'});
					cell.data('index', j);
					cell.data('diagnostic', false);
					var btn = $("<button> Random </button>", {'class': 'stimUI-btn'});
					cell.append(btn);
					btn.click(function(e) {
						if(cell.data('diagnostic') === false){
							cell.data('diagnostic', true);
							cell.text(' Invariant ');
							selectColumn(cell.data('index')).addClass('stimUI-chosen');
						}
						else{
							cell.data('diagnostic', false);
							cell.text(' Random ');
							selectColumn(cell.data('index')).removeClass('stimUI-chosen');
						}
					});
				}
				
				row.append(cell);
			}
			controller[i] = contRow;
			table.append(row)
		}
		return table;
	}
	
	/**
	 * Initializes the widget and inserts the UI into the page
	 * 
	 * @param	{jQuery.fn} $target	the element that will hold the UI.
	 */
	core.init = function(){
		//append the overall container
		target.append(ui);
		loadImages(function(){
			ui.append(core.build(6));
		});
	}
	
	
	return core;
}