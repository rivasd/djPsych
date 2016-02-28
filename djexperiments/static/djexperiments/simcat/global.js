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
       
        djPsych.request('test', run);
        
    }
    
    function augment(data, exp){
    	data.parameters = exp.parameters;
    	data.complete = true;
    }
    
    function run(settings){
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
			$("#stimCanvas").remove();
    		//HERE IS WHERE THE EXPERIMENT BEGINS
    		jsPsych.init({
    			display_element: $("#jsPsychTarget"),
    			timeline: exp.timeline,
    			on_finish: function(data){
    				jsPsych.data.displayData("json");
    				djPsych.save(data, augment, exp.meta);
    			}
    		})
		})
	}
    
    $("#start").click(function (e) {
        if (document.getElementById("accept").checked) {
            var top = document.getElementById("top").offsetTop;
            window.scrollTo(0, top);
            $("#consent").remove();
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