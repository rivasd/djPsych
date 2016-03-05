$(function () {

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

    function runExperiment() {
    	//we need the progress bar and the canvas
    	var $progressbar = $("<div></div>", {id:'progressBar'});
    	var $stimCanvas = $("<canvas></canvas>", {id: 'stimCanvas', height: 300, width: 300});
    	var $feedback = $("<div></div>", {id: 'retroaction'});
    	$("#content").prepend($feedback);
    	$("#jsPsychTarget").append($progressbar).append($stimCanvas);
        djPsych.request(run);
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
			// Test code to test for unexpected
			// jsPsych.data.addProperties({dummy: 'lol'}) yay my code works for arbitrary extra data!
			
    		jsPsych.init({
    			display_element: $("#jsPsychTarget"),
    			timeline: exp.timeline,
    			on_finish: function(data){
    				jsPsych.data.displayData("json");
    				djPsych.save(data, true);
    			}
    		})
		})
	}

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