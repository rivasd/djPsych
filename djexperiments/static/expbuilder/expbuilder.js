/**
 * Defines namespace and initiate the expBuilder app
 */
<<<<<<< Upstream, based on branch 'Backbone' of https://github.com/rivasd/djPsych.git


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

=======
>>>>>>> 8c812e9 starting to develop backbone models
