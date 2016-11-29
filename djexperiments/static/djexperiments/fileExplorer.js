/**
 * Provides jsTree functionality to the experiment control panel
 */


$(function(){
	
	var fileExp = $("#djpsych-explorer").jstree({
		plugins: ["contextmenu", "types"],
		contextmenu:{
			show_at_node:false,
			items: buildContextItems
		},
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
			},
			"folder":{
				icon: 'fa fa-folder-o'
			},
			"css":{
				icon: 'fa fa-paint-brush'
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
			},
			check_callback: true
		}
	});
	
	//data transfer through semi-global variables.... sorry
	var currentlyEditedNode;
	
	
	function buildContextItems($node){
		var tree = $("#djpsych-explorer").jstree();
		var default_menu =  {
			"AddFile": {
                "separator_before": false,
                "separator_after": false,
                "label": "Add file",
                "action": function (data) { 
                	var inst = $.jstree.reference(data.reference);
                	var obj = inst.get_node(data.reference);
                	var parent; //set argument needed for server-side code
                	if(obj.type=="#"){
                		parent = "";
                	}
                	else{
                		parent = obj.data;
                	}
                	//set a global variable so that code outside this scope can change the tree after server response
                	currentlyEditedNode = data;
                	
                	$("#parentFolder").val(parent)
                	$("#action").val("add")
                	fileDialog.showModal();
                }
            },
            "AddFolder":{
                "separator_before": false,
                "separator_after": false,
                "label": "Add folder",
                "action": function (data) { 
                	var inst = $.jstree.reference(data.reference);
                	var obj = inst.get_node(data.reference);
                	
                	inst.create_node(obj, {type:'folder', text:"newFolder"}, "last", function (new_node) {
						setTimeout(function () { inst.edit(new_node); },0);
					});
                }
            },
            "Rename": {
                "separator_before": false,
                "separator_after": false,
                "label": "Rename",
                "action": function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
					currentlyEditedNode = data
					inst.edit(obj);
                }
            },                         
            "Remove": {
                "separator_before": false,
                "separator_after": false,
                "label": "Delete",
                "action": function (data) {
					var inst = $.jstree.reference(data.reference),
					obj = inst.get_node(data.reference);
					var selection;
					var to_delete=[];
					if(inst.is_selected(obj)) {
						selection = inst.get_selected(true).map(function(node){return node.data});
						to_delete = inst.get_selected()
					}
					else {
						selection = [obj.data]
						to_delete = obj
					}
					$.ajax({
						method:"POST",
						url: 'files',
						dataType:"json",
						data:{
							action: "rm",
							args : JSON.stringify(selection)
						},
						success: function(resp){
							if(resp.success){
								inst.delete_node(to_delete)
							}
							else{
								alert(resp.error)
							}
						}
					})
					
                }
            }
		}
		
		var final_menu = default_menu;
		if($node.type == "#"){
			delete final_menu["Rename"];
			delete final_menu["Remove"]
		}
		else if($node.type == "folder"){
			delete final_menu["AddFolder"]
		}
		else {
			delete final_menu["AddFile"];
			delete final_menu["AddFolder"];
		}
		return final_menu
	}
	
	fileExp.on("rename_node.jstree", function(e, data){
		alert("hey!");
		//do the renaming server-side!
		/*
		$.ajax({
			method: 'post',
			url: 'files',
			dataType: 'json',
			data:{
				action: 'rename',
				target: data.node.data,
				name: data.text
			}
		});
		*/
	});
	
	
	//code for  the file upload <dialog> element
	var fileDialog = document.getElementById("djpsych-upload-dialog");
    if (! fileDialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    fileDialog.querySelector(".close").addEventListener('click', function(){
    	fileDialog.close();
    });
    
    $("#djpsych-upload-dialog__submit").click(function(evt){
    	evt.preventDefault();
    	var form = new FormData(document.getElementById("djpsych-upload-dialog__form"))
    	$.ajax({
    		method:"post",
    		url: "files",
    		dataType: "json",
    		success: function(resp){
    			if(resp.success){
    				
    				var inst = $.jstree.reference(currentlyEditedNode.reference);
                	var obj = inst.get_node(currentlyEditedNode.reference);
                	resp.nodes.forEach(function(node){
                		inst.create_node(obj, node, "last");
                	});
    				
    				currentlyEditedNode = undefined;
    				fileDialog.close();
    			}
    			else{
    				alert(resp.error);
    			}
    		},
    		data:form,
    		processData: false,
    		contentType: false,
    		cache: false
    	});
    });
    
});