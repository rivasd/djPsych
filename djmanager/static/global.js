$(function () {


    //preload the little spinner
    var spinner = document.createElement('img');
    spinner.src = "style/stimCreationLoader.gif";



    $.fn.clicktoggle = function (a, b) {
        return this.each(function () {
            var clicked = false;
            $(this).click(function () {
                if (clicked) {
                    clicked = false;
                    return b.apply(this, arguments);
                }
                clicked = true;
                return a.apply(this, arguments);
            });
        });
    };

    function letsGo(pageText, target, paintingArea) {
        var toKill = document.getElementById(pageText);
        toKill.parentNode.removeChild(toKill);
        //NEW CODE HERE!!
        var before = $("#start").html();
        $("#start").html('<img src="/static/style/ajax-loader.gif"/>');
       
        $.ajax('load', {
        	dataType: "json", //because that is what we expect from our server
        	data: {type: 'test'},
        	error: function(){
        		alert("someone tell the webmaster his server is broken...");
        	},
        	success: function(settings){
        		var launcher = ExpLauncher(settings, document.getElementById("stimCanvas")); //initialize a launcher and drawer 
        		var $bar = $("#progressBar");
        		$bar.progressbar({
        			max : settings.timeline[0].length
        		});
        		function increment(idx, total){
        			$bar.progressbar("value", idx);
        		};
        		launcher.loadMicroComponents(settings, function(){
        			var exp = launcher.createStandardExperiment(settings, increment, {reuseStim: true, saveDescription: true});
            		exp.meta.startTime = new Date().toISOString();
        			$bar.progressbar("destroy");
            		//HERE IS WHERE THE EXPERIMENT BEGINS
            		jsPsych.init({
            			display_element: $("#jsPsychTarget"),
            			timeline: exp.timeline,
            			on_finish: function(data){
            				jsPsych.data.displayData("json");
            				sendAway({meta: exp.meta, data: data}, postSave);
            			}
            		})
        		})
        	}
        });
        
    }
    
    function sendAway(data, callback){
    	$.ajax({
    		url: 'save',
    		data:{
    			meta: JSON.stringify(data.meta),
    			data: JSON.stringify(data.data)
    		},
    		dataType: 'json',
    		methos: 'POST',
    		type: 'POST',
    		success: function(response){
    			if(callback) callback(response);
    		}
    	})
    }
    
    
    function postSave(response){
    	if(response['error']){
    		alert(response.error);
    	}
    	else if(response['success']){
    		alert(response.success);
    	}
    }
    
    $("#start").click(function (e) {
        if (document.getElementById("accept").checked) {
            var top = document.getElementById("top").offsetTop;
            window.scrollTo(0, top);
            var theCanvas = document.getElementById("stimCanvas");
            letsGo("instructionsUp", "#jsPsychTarget", theCanvas);
            $('#start').remove();
        }
        else {
            alert("veuillez cocher la case J'accepte / Please check the box I Accept");
        }

    });

    $("span.expand").html("[+] ");
    $(".entryBody").hide();


    $("h4.entryTitle").clicktoggle(function () {
        $(this).next(".entryBody").slideDown();
        $(this).children(".expand").html("[-] ");
    }, function () {
        $(this).next(".entryBody").slideUp();
        $(this).children(".expand").html("[+] ");
    });

    //global (i know...) variable keeping track of whether this is the first time the ques
    var isFirstQuestionnaire = true;

    $("#dldstim").click(function () {
        var experiment = new ExperimentManager("#jsPsycTarget");
        experiment.getStim(document.getElementById("stimCanvas"));
    });

});