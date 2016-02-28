/**
 * A little utility module meant to ease communication between a djPsych server and jsPsych.
 * @see {@link https://github.com/rivasd/djPsych}
 * @requires jQuery
 * @requires jQuery-UI
 */
var djPsych = (function djPsych($){
	var core ={};
	var expLabel = "";
	var staticUrl = "";
	var prefix = "";
		
	var meta = "";
	
	function get_browser_info(){
	    var ua=navigator.userAgent,tem,M=ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || []; 
	    if(/trident/i.test(M[1])){
	        tem=/\brv[ :]+(\d+)/g.exec(ua) || []; 
	        return {name:'IE',version:(tem[1]||'')};
	        }   
	    if(M[1]==='Chrome'){
	        tem=ua.match(/\bOPR\/(\d+)/)
	        if(tem!=null)   {return {name:'Opera', version:tem[1]};}
	        }   
	    M=M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
	    if((tem=ua.match(/version\/(\d+)/i))!=null) {M.splice(1,1,tem[1]);}
	    return {
	      name: M[0],
	      version: M[1]
	    };
	 }
	
	/**
	 * Initialize the djPSych.js module by pointing it to the right URLs for communicating with the server
	 * @param {String} expLabel		When you created your Experiment object on djPsych, this is the label field. your experiment lives at this URL
	 * @param {String} staticRoot	corresponds to the STATIC_URL setting in the settings.py of the server. tells us where to fetch static content.
	 */
	core.init = function init(name, staticRoot){
		expLabel = name;
		staticUrl = staticRoot;
		prefix = staticUrl+'djexperiments/'+expLabel+'/';
	}
	
	core.getPrefix = function(){
		return prefix;
	}
	
	core.prefix = function(path){
		return prefix+path;
	}
	
	/**
	 * Requests a setting object from the server in order to start an experiment. 
	 * @param {string} 		version		A string indicating the 'name' field of the global setting object to fetch from the server. With this you can choose which version of the experiment to fetch
	 * @param {function}	callback	A function to execute after receiving an answer. Will be called only if the server does not respond with an error. Default behavior is to display a dialog box with the error content. Receives the full server answer as the sole argument
	 */
	core.request = function request(version, callback){
		$.ajax({
			data:{
				version: version
			},
			dataType: 'json',
			error: function(jqHXR, status, thrown){
				alert("server could not be reached at: /webexp/"+expLabel+'/request\n\nError: '+status+' thrown');
			},
			method: 'GET',
			success: function(resp){
				if(resp.error != undefined){
					$("<div><p>ERROR</p><p>"+resp.error+"</p></div>").dialog({
						modal:true
					});
				}
				else{
					meta = resp;
					callback(resp)
				}
			},
			url: '/webexp/'+expLabel+'/request'
		});
	}
	
	/**
	 * Sends collected data back to the server to be saved, taking care of filling the meta object based on what was received by the previous .request() call.
	 * Displays a jquery-ui dialog box to indicate the result of the operation with a link towards the profile page.
	 * @param	{jsPsych-data}	data		An array of objects as returned by a call to jsPsych.data.getData() or like the sole argument to the on_finish callback that can be passed to jsPsych.init()
	 * @param	{function=}		lastChance	Optional function that can be called on the full payload (e.g. containing both data and meta) just before sending it away. Must do changes in-place, return value will be ignored
	 * @param	{*=}			local		the lastChance function will be called with this as second parameter if given
	 */
	core.save = function save(data, lastChance, local){
		if(meta == "" || meta==undefined){
			alert("metadata was not set by a previous call to djPsych.request");
		}
		var $dialog = $('<div><p>Sending data...</p><img src="'+staticUrl+'style/ajax-loader.gif" height="10px" width="10px"/></div>');
		$dialog.dialog({
			modal:true,
			closeOnEscape: false,
			draggable: false
		})
		
		payload = {};
		payload.data = data;
		metadata = {};
		metadata.browser = get_browser_info();
		metadata.name= meta.name;
		metadata.subject = meta.subject;
		metadata.current_exp = meta.current_exp;
		metadata.exp_id = meta.exp_id;
		metadata.previous = meta.previous;
		payload.meta = metadata;
		if(typeof lastChance != undefined){
			lastChance(payload, local);
		}
		$.ajax({
			url: '/webexp/'+expLabel+'/save',
			method: 'POST',
			type: 'POST',
			data: {
				data: JSON.stringify(payload.data),
				meta: JSON.stringify(payload.meta)
			},
			dataType: 'json',
			error: function(jqHXR, status, thrown){
				$dialog.html("server could not be reached at: /webexp/"+expLabel+'/save\n\nError: '+status+' '+thrown);
			},
			success: function(resp){
				$dialog.html("<p>"+resp.success+'</p><p><a href="/webexp">'+"Back to homepage"+'</a>');
			}
		});
	}
	
	return core
})(jQuery)