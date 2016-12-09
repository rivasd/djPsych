/**
 * Defines namespace and initiate the expBuilder app
 */



	var expBuilder = {
		
		module: function(){
			var modules = {};
			
			return function(name){
				
				if(modules[name]){
					
					return modules[name];
				}
				
				return modules[name] = {Views:{}};
			}
		}
	}


