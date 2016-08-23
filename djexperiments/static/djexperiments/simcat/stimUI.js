
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
		
		var mc = $("<img>", {id: 'microcomp-'+row+'-'+col, class: 'stimUI-thumbnail', width:36, heigth: 36});
		var selector = $("<select>");
		microcomponents.forEach(function(elt, i, array) {
			var option = $("<option>", {label: elt, value: '/static/djexperiments/simcat/attributes/'+elt});
			
			option.on("focus", function(e){
				mc.src = this.value;
			});
			
			selector.append(option);
		});
		$cell.append(mc).append(selector);
		
	}
	
	
	/**
	 * Creates the table element that will hold our microcomponents and holds it in memory. DOES NOT insert it in the DOM 
	 */
	core.build = function(len){
		table = $("<table></table>", {class:'stimUI-table'});
		for(var i=0;i<2;i++){
			var row = $("<tr></tr>");
			var contRow = []
			for(var j=0;j<len;j++){
				
				cell = createCell(i, j);
				contRow.push(cell);
				row.append(cell);
				cell.on('dragover', function(evt){
					evt.dataTransfer.dropEffect = 'move';
					evt.preventDefault();
				});
				cell.on('drop', handleDrop);
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
			
		});
		
		
		
		ui.append(core.build(6));
	}
	
	
	return core;
}