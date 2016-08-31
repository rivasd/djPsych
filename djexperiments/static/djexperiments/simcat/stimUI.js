
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
	
	var ui = $("#stimUI-config");
	var densityInput;
	var quantityInput;
	var renderer;
	
	
	
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
	
	function addCol(){
		var currLength = table.find("tr.stimUI-row").first().find("td").length;
		$("#stimUI-row-0").append(createCell(0, currLength));
		$("#stimUI-row-1").append(createCell(1, currLength));
		$("#stimUI-row-2").append(createBtnCell(currLength));
	}
	
	function rmvCol(){
		
		var currLength = table.find("tr.stimUI-row").first().find("td").length;
		if(currLength <= 4){
			return;
		}
		$("td.stimUI-cell").filter(function(idx, elem){
			return $(elem).data('index')[1] === currLength-1;
		}).remove();
		$("#stimUI-status-"+(currLength-1)).remove();
	}
	
	
	/**
	 * Generates a table cell with all the UI needed to make it represent a settable micro-components
	 * @private
	 */
	function createCell(row, col){
		var $cell = $("<td></td>", {class:'stimUI-cell'});
		$cell.data('index', [row,col]);
		
		var mc = $("<img>", {id: 'microcomp-'+row+'-'+col, class: 'stimUI-thumbnail'});
		
//		mc.attr('width', 36);
//		mc.attr('height', 36);
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
	
	function createBtnCell(index){
		var cell = $("<td></td>", {'class': 'stimUI-invariant', 'id':'stimUI-status-'+index});
		cell.data('index', index);
		cell.data('diagnostic', false);
		var btn = $("<button> Random </button>", {'class': 'stimUI-btn'});
		cell.append(btn);
		btn.click(function(e) {
			var contcell = $(this).parent();
			if(contcell.data('diagnostic') === false){
				contcell.data('diagnostic', true);
				this.textContent=' Invariant ';
				selectColumn(contcell.data('index')).addClass('stimUI-chosen');
			}
			else{
				contcell.data('diagnostic', false);
				this.textContent = ' Random ';
				selectColumn(contcell.data('index')).removeClass('stimUI-chosen');
			}
		});
		
		return cell;
	}
	
	
	/**
	 * Selects all td elements that make up the requested column in the table
	 * @private
	 * @param 	{number} 	idx		the 0-based index of the column to select
	 * @return	{jQuery.fn}			a jQuery selection of the td elements that make up the column
	 */
	function selectColumn(idx){
		return $("#stimUI-table td").filter(function(i, elm){
			return $(elm).data('index')[1] === idx;
		});
	}
	
	
	/**
	 * Creates the table element that will hold our microcomponents and holds it in memory. DOES NOT insert it in the DOM 
	 */
	core.build = function(len){
		table = $("<table></table>", {id:'stimUI-table'});
		for(var i=0;i<3;i++){
			var row = $("<tr></tr>", {'class': 'stimUI-row', id:'stimUI-row-'+i});
			var contRow = []
			for(var j=0;j<len;j++){
				
				var cell;
				if(i<2){
					cell = createCell(i, j);
					contRow.push(cell);
				}
				else{
					cell = createBtnCell(j);
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
		loadImages(function(){
			target.replaceWith(core.build(6));
			var addBtn = $("#stimUI-addcolbtn");
			var rmvBtn = $("#stimUI-rmvcolbtn");
			densityInput = $("#stimUI-density");
			quantityInput = $("#stimUI-quantity");
			var renderBtn = $("#stimUI-renderbtn");
			//event listeners for our UI buttons
			addBtn.click(addCol);
			rmvBtn.click(rmvCol);
			
			renderBtn.click(function(e){
				core.render();
			});
		});
		ui.submit(function(evt) {
			evt.preventDefault();
			//return false;
		})
	}
	
	/**
	 * 
	 */
	core.render = function(){
		var tableLength = table.find("tr").first().find("td").length;
		var invariants = 0;
		
		var microcomponents = {};
		var definitions = {
				'lakamite': {},
				'kalamite': {}
		};
		
		for(var i=0;i<tableLength;i++){
			var pair = selectColumn(i);
			var firstTd = pair.slice(0,1);
			var secndTd = pair.slice(1);
			var statusCell = $("#stimUI-status-"+i);
			
			microcomponents[i] = {
					0: firstTd.children("img")[0],
					1: secndTd.children("img")[0]
			};
			
			if(statusCell.data('diagnostic') === true){
				invariants++;
				definitions['lakamite'][i]=0;
				definitions['kalamite'][i]=1;
			}
			else{
				definitions['lakamite'][i]='free';
				definitions['kalamite'][i]='free';
			}
		}
		
		renderer = StimEngine({
			'microcomponents': microcomponents, 
			'types': definitions,
			'width': densityInput.val(),
			'height': densityInput.val(),
		}, document.getElementById("board"));
		
		var distances = []
		//divide the number of pairs requested evenly among the possible distances
		for(var i=0; i <= (tableLength - invariants); i++){
			distances[i] = Math.floor(quantityInput.val() / (tableLength-invariants + 1));
		}
		//there might be a remainder, just place it somewhere
		for(var j=0; j < (quantityInput.val() % (tableLength - invariants +1)); j++){
			distances[j] = distances[j] + 1;
		}
		//initialize the zip file
		var mainZip = new JSZip();
		
	
		distances.forEach(function(elt, i, array) {
			for(var j=0;j<elt;j++){
				//a little modulo magic to evenly-ish distribute among all possible pairs (same-different)
				var type = j % 4;
				var firstType = type > 1 ? 'lakamite' : 'kalamite';
				var scndType = type % 2 == 0 ? 'lakamite' : 'kalamite';
				//draw the pairs and give them a "sensible" name
				var imgVectors = renderer.generateVectorPair(definitions[firstType], definitions[scndType], i);
				var imgPair = renderer.drawPair(imgVectors[0], imgVectors[1]);
				var firstImgName = firstType+'-dist'+i+'-pair'+j+'-A.png';
				var secndImgName = scndType + '-dist'+i+'-pair'+j+'-B.png';
				
				mainZip.folder(firstType).file(firstImgName, imgPair[0].substring(imgPair[0].indexOf(',')), {base64:true});
				mainZip.folder(scndType).file(secndImgName, imgPair[1].substring(imgPair[1].indexOf(',')), {base64:true});
			}
		});
		
		//force download of the zip archive
		mainZip.generateAsync({type:'blob'}).then(function(blob){
			saveAs(blob, 'textures.zip');
		});
	}
	
	return core;
}