/**
 * Everything you need for the block model is here
 */

(function(expBuilder, Block) {
	
	//Dependencies
	//Shorthands
	//The application container
	
	
	//Define a basic block (with all the attributes all the blocks have in common)
	Block.Model = Backbone.Model.extends({
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
	
	
	
})(expBuilder, expBuilder.module("block"))