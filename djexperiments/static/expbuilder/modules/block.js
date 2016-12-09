
/**
 * Everything you need for the block models is here
 */
	

	
	
	//Define a basic block (with all the attributes all the blocks have in common)
	var block = Backbone.Model.extends({
		defaults: {
			id: null,
			content_type: null,
			name: null,
			position_in_timeline: null,
			length: null,
			type: null,
			has_practice: null,
			extra_params: null			
		}
	
		
	});
	
	var audioCatBlock = Block.extends({
		
	});
	
	
	
	
	
