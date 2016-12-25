

/**
 * Everything you need for the block models is here
 */
	var module = (function(){
		
		var block = Backbone.Model.extends({
			//TODO add usefull methods here
		});
		
		var configuration = Backbone.Collection.extends({
			model : block
			//TODO adding api end point (sync function?)
		});
		
		return module;
		
	})();

	
	
	
	

