/**
 * Provides jsTree functionality to the experiment control panel
 */


$(function(){
	
	$("#djpsych-explorer").jstree({
		plugins: ["checkbox", "wholerow", "types"],
		types:{
			"js":{
				icon: "fa fa-cogs",
				max_childre:0
			},
			"#":{
				max_depth: 2
			},
			"image":{
				icon:"fa fa-file-image-o"
			}
		},
		core:{
			data:{
				url:'files',
				dataType: 'json',
				method: 'POST',
				data:{
					action: 'ls',
					mode: 'jsTree'
				}
			}
		}
	});
});