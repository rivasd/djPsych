/**
 * jspsych-similarity.js
 * Josh de Leeuw
 *
 * This plugin create a trial where two images are shown sequentially, and the subject rates their similarity using a slider controlled with the mouse.
 *
 * documentation: docs.jspsych.org
 *
 */


jsPsych.plugins.similarity = (function() {

  var plugin = {};

  jsPsych.pluginAPI.registerPreload('similarity', 'stimuli', 'image');

  plugin.trial = function(display_element, trial) {

    // default parameters
    trial.labels = (typeof trial.labels === 'undefined') ? ["Not at all similar", "Identical"] : trial.labels;
    trial.intervals = trial.intervals || 100;
    trial.show_ticks = (typeof trial.show_ticks === 'undefined') ? false : trial.show_ticks;

    trial.show_response = trial.show_response || "SECOND_STIMULUS";

    trial.timing_first_stim = trial.timing_first_stim || 1000; // default 1000ms
    trial.timing_second_stim = trial.timing_second_stim || -1; // -1 = inf time; positive numbers = msec to display second image.
    trial.timing_image_gap = trial.timing_image_gap || 1000; // default 1000ms
    trial.timing_fixation_cross = trial.timing_fixation_cross||1500;
    trial.timeout = trial.timeout || 3000 //amount of time the response slider will be showing
    trial.timeout_message = trial.timeout_message || "<p>Please respond faster</p>";
    trial.timeout_message_timing = trial.timeout_message_timing || 1000;
    
    trial.is_html = (typeof trial.is_html === 'undefined') ? false : trial.is_html;
    trial.prompt = (typeof trial.prompt === 'undefined') ? '' : trial.prompt;
    
    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);
    
    //Adding new parameters 
    plugin.sample_page = plugin.sample_page || true;
    
    
    
    /**
     * Let's try out my idea of normalizing trial logic as trial methods
     * the action that happens when a trial is run should all be encapsulated inside methods of the trial object
     * By doing this, we can implement an API of trial-action that will allow developers to tweak the logic more easily
     * this way we can easily reuse code for common actions to do inside a trial, easily change order, and decorated functions!
     * @author Daniel Rivas
     */
    
    //Added feature to prevent returning the stimulus in case it a dynamically-created one and thus potentially huge
    trial.return_stim = (typeof trial.return_stim == 'undefined') ? true : trial.return_stim;
    
    // this array holds handlers from setTimeout calls
    // that need to be cleared if the trial ends early
    trial.setTimeoutHandlers = [];
    
    function showFixationCross(){
    	display_element.empty();
    
    	if(display_element.css("position")==="static"){
    		display_element.css("position", "relative");
    	}
    	
        var $paragraph = $("<p>+</p>");
        display_element.append($paragraph);
        $paragraph.css({
        	"font-size":"350%",
    	    "position":"absolute",
    	    "left": "50%",
    	    "top": "50%",
    	    "transform": "translate(-50%, -50%)"   
        });  	
    }
    
    
    showFixationCross();
    
    setTimeout(function(){
    	display_element.empty();
    	showFirstImage();  	
    }, trial.timing_fixation_cross);
   
    
    function showFirstImage(){
    // show the images
	    if (!trial.is_html) {
	      display_element.append($('<img>', {
	        "src": trial.stimuli[0],
	        "id": 'jspsych-sim-stim'
	      }));
	    } else {
	      display_element.append($('<div>', {
	        "html": trial.stimuli[0],
	        "id": 'jspsych-sim-stim'
	      }));
	    }
	    
	    //first stimuli has been shown, send first trigger
	    if(trial.hardware_first_stim && jsPsych.pluginAPI.hardwareConnected){
	    	jsPsych.pluginAPI.hardware(trial.hardware_first_stim);
	    }
	
	    if (trial.show_response == "FIRST_STIMULUS") {
	      show_response_slider(display_element, trial);
	    }
	
	    trial.setTimeoutHandlers.push(setTimeout(function() {
	      showBlankScreen();
	    }, trial.timing_first_stim));
    }

    function showBlankScreen() {

      $('#jspsych-sim-stim').css('visibility', 'hidden');

      trial.setTimeoutHandlers.push(setTimeout(function() {
        showSecondStim();
      }, trial.timing_image_gap));
    }

    function showSecondStim() {

      if (!trial.is_html) {
        $('#jspsych-sim-stim').attr('src', trial.stimuli[1]);
      } else {
        $('#jspsych-sim-stim').html(trial.stimuli[1]);
      }

      $('#jspsych-sim-stim').css('visibility', 'visible');
      
      //second stimuli has been shown, send trigger
      
      if(trial.hardware_second_stim && jsPsych.pluginAPI.hardwareConnected){
      	jsPsych.pluginAPI.hardware(trial.hardware_second_stim);
      }
      
      
      if(trial.show_response == "SECOND_STIMULUS") {
          show_response_slider(display_element, trial);
      }
      
      if (trial.timing_second_stim > 0) {
        trial.setTimeoutHandlers.push(setTimeout(function() {
          $("#jspsych-sim-stim").css('visibility', 'hidden');
          if (trial.show_response == "POST_STIMULUS") {
            show_response_slider(display_element, trial);
          }
        }, trial.timing_second_stim));
      }
    }
    
    
    function endTrial(data){
        

        // kill any remaining setTimeout handler
	        for (var i = 0; i < trial.setTimeoutHandlers.length; i++) {
	          clearTimeout(trial.setTimeoutHandlers[i]);
	        }
        
	    trial_data.timeout = false; //quick hack for something I need right now
	    if(data.sim_score === undefined){
	    	data.sim_score = 0;
	    	data.timeout = true;
	    }
	    
        
        if(trial.return_stim){
        	data.stimulus = JSON.stringify([trial.stimuli[0], trial.stimuli[1]]);
        }
        // goto next trial in block
        display_element.html('');
        
        if(data.rt === -1){
        	//this was a timeout
        	display_element.append(trial.timeout_message);
        	trial.setTimeoutHandlers.push(setTimeout(function(){
        		display_element.empty();
        		jsPsych.finishTrial(data);
        	},trial.timeout_message_timing))
        }
        else{
        	jsPsych.finishTrial(data);
        }
        
        
     }


    function show_response_slider(display_element, trial) {

      var startTime = (new Date()).getTime();

      // create slider
      display_element.append($('<div>', {
        "id": 'slider',
        "class": 'sim'
      }));

      $("#slider").slider({
        value: Math.ceil(trial.intervals / 2),
        min: 1,
        max: trial.intervals,
        step: 1,
      });

      // show tick marks
      if (trial.show_ticks) {
        for (var j = 1; j < trial.intervals - 1; j++) {
          $('#slider').append('<div class="slidertickmark"></div>');
        }

        $('#slider .slidertickmark').each(function(index) {
          var left = (index + 1) * (100 / (trial.intervals - 1));
          $(this).css({
            'position': 'absolute',
            'left': left + '%',
            'width': '1px',
            'height': '100%',
            'background-color': '#222222'
          });
        });
      }

      // create labels for slider
      display_element.append($('<ul>', {
        "id": "sliderlabels",
        "class": 'sliderlabels',
        "css": {
          "width": "100%",
          "height": "3em",
          "margin": "10px 0px 0px 0px",
          "padding": "0px",
          "display": "block",
          "position": "relative"
        }
      }));

      for (var j = 0; j < trial.labels.length; j++) {
        $("#sliderlabels").append('<li>' + trial.labels[j] + '</li>');
      }

      // position labels to match slider intervals
      var slider_width = $("#slider").width();
      var num_items = trial.labels.length;
      var item_width = slider_width / num_items;
      var spacing_interval = slider_width / (num_items - 1);

      $("#sliderlabels li").each(function(index) {
        $(this).css({
          'display': 'inline-block',
          'width': item_width + 'px',
          'margin': '0px',
          'padding': '0px',
          'text-align': 'center',
          'position': 'absolute',
          'left': (spacing_interval * index) - (item_width / 2)
        });
      });

      //  create button
      display_element.append($('<button>', {
        'id': 'next',
        'class': 'sim',
        'html': 'Submit Answer'
      }));
       
      // if prompt is set, show prompt
      if (trial.prompt !== "") {
        display_element.append(trial.prompt);
      }  
      
      trial.setTimeoutHandlers.push(setTimeout(function(){
    	  endTrial({rt:-1});
      }, trial.timeout));
      
      
      
      $("#next").click(function(){
    	  var endTime = (new Date()).getTime();
          var response_time = endTime - startTime;
    	  endTrial({
    		  rt: response_time,
    		  sim_score: $("#slider").slider("value")
    	  });
      });
    }
  };
  return plugin;
  })();
