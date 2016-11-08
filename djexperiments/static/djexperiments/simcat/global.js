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

    
    function augment(data, exp){
    	data.parameters = exp.parameters;
    	data.complete = true;
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

});

function run(settings){
	settings.timeline = serverPsych.unpack(settings.timeline, function(t){return t;});
	var launcher = ExpLauncher(settings, document.getElementById("stimCanvas")); //initialize a launcher and drawer 
	var $bar = $("#progressBar");
	var $progressLabel = $("<div></div>");
	$progressLabel.html(loading);
	$("#jsPsychTarget").append($progressLabel);
	
	$bar.progressbar({
		value :false
	});

	launcher.loadMicroComponents(settings, function(){
		var exp = launcher.createStandardExperiment(settings, null, {reuseStim: true, saveDescription: true});
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
				//jsPsych.data.displayData("json");
				serverPsych.save(data, true, exp.meta);
			},
			on_trial_start:function(){
				jsPsych.getDisplayElement()[0].scrollIntoView();
			}
		})
	})
}

function runExperiment() {
	//we need the progress bar and the canvas
	var $progressbar = $("<div></div>", {id:'progressBar'});
	var $stimCanvas = $("<canvas></canvas>", {id: 'stimCanvas', height: 300, width: 300});
	var $feedback = $("<div></div>", {id: 'retroaction'});
	$("#content").prepend($feedback);
	$("#jsPsychTarget").append($progressbar).append($stimCanvas);
    serverPsych.request(run, 'final');
}

function showWinnings(trial_data){
	
}

//TODO: make sure that you cannot advance past questionnaire trial without filling appropriate fields


