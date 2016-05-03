
/**
 * A widget for allowing users to generate sets of our stimuli while controlling the properties through a GUI
 * 
 * @param	{jQuery}	target	a jQuery selection of the the element that will hold this widget
 * @author Daniel Rivas
 * @date 2016-04-27
 */
function StimUI(target){
	var core={};
	var backend;
	var diagnostic;
	
	var cells;
	var table;
	var controller = new Array(2);
	
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
	 * Creates the table element that will hold our microcomponents and holds it in memory. DOES NOT insert it in the DOM 
	 */
	core.build = function(len){
		table = $("<table></table>", {class:'stimui-table'});
		for(var i=0;i<2;i++){
			var row = $("<tr></tr>");
			var contRow = []
			for(var j=0;j<len;j++){
				var cell = $("<td></td>", {class:'stimui-cell'});
				cell.data('index', [i,j]);
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
	}
	
	
	
	
	return core;
}