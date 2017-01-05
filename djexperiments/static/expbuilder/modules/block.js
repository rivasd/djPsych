

/**
 * Everything you need for the block models is here
 */
	var module = (function(){
		
		var blockIdentifier = function (attr, options){
			switch (attr.type){
				case 'animation':
					return new AnimationBlock(model, options);
				case 'audio-categorization':
					return new AudioCategorizationBlock(model, options);
				case 'audio-similarity':
					return new AudioSimilarityBlock(model, options);
				case 'button-response':
					return new ButtonResponseBlock(model, options);
				case 'categorize-animation':
					return new CategorizeAnimationBlock(model, options);
				case 'categorize':
					return new CategorizeBlock(model, options);
				case 'forcedchoice':
					return new ForcedChoiceBlock(model, options);
				case 'free-sort':
					return new FreeSortBlock(model, options);
				case 'html':
					return new HTMLBlock;
				case 'multi-stim-multi-response':
					return new MultiStimMultiResponseBlock(model, options);
				case 'rating':
					return new RatingBlock(model, options);
				case 'reconstruction':
					return new ReconstructionBlock(model, options);
				case 'same-different':
					return new SameDifferentBlock(model, options);
				case 'similarity':
					return new SimilarityBlock(model, options);
				case 'single-audio':
					return new SingleAudioBlock(model, options);
				case 'single-stim':
					return new SingleStimBlock(model, options);
				case 'survey-likert':
					return new SurveyLikertBlock(model, options);
				case 'survey-multi-choice':
					return new SurveyMultiChoiceBlock(model, options);
				case 'survey-text':
					return new SurveyTextBlock(model, options);
				case 'xab':
					return new XABBlock(model, options);		
			}
		}
		
		var AnimationBlock = Backbone.Model.extend({
			defaults: {
				type: 'animation'
			}
		});
		
		var AudioCategorizationBlock = Backbone.Model.extend({
			defaults: {
				type: 'audio-categorization'
			}
		});
		
		var AudioSimilarityBlock = Backbone.Model.extend({
			defaults: {
				type: 'audio-similarity'
			}
		});
		
		var ButtonResponseBlock = Backbone.Model.extend({
			defaults: {
				type: 'button-response'
			}
		});
		
		var CategorizeAnimationBlock = Backbone.Model.extend({
			defaults: {
				type: 'categorize-animation'
			}
		});
		
		var CategorizeBlock = Backbone.Model.extend({
			defaults: {
				type: 'categorize'
			}
		});
		
		var ForcedChoiceBlock = Backbone.Model.extend({
			defaults: {
				type: 'forcedchoice'
			}
		});
		
		var FreeSortBlock = Backbone.Model.extend({
			defaults: {
				type: 'free-sort'
			}
		});
		
		var HTMLBlock = Backbone.Model.extend({
			defaults: {
				type: 'html'
			}
		});
		
		var MultiStimMultiResponseBlock = Backbone.Model.extend({
			defaults: {
				type: 'multi-stim-multi-response'
			}
		});
		
		var RatingBlock = Backbone.Model.extend({
			defaults: {
				type: 'rating'
			}
		});
		
		var ReconstructionBlock = Backbone.Model.extend({
			defaults: {
				type: 'reconstruction'
			}
		});
		
		var SameDifferentBlock = Backbone.Model.extend({
			defaults: {
				type: 'same-different'
			}
		});
		
		var SimilarityBlock = Backbone.Model.extend({
			defaults: {
				type: 'similarity'
			}
		});
		
		var SingleAudioBlock = Backbone.Model.extend({
			defaults: {
				type: 'single-audio'
			}
		});
		
		var SingleStimBlock = Backbone.Model.extend({
			defaults: {
				type: 'single-stim'
			}
		});
		
		var SurveyLikertBlock = Backbone.Model.extend({
			defaults: {
				type: 'survey-likert'
			}
		});
		
		var SurveyMultiChoiceBlock = Backbone.Model.extend({
			defaults: {
				type: 'survey-multi-choice'
			}
		});
		
		var SurveyTextBlock = Backbone.Model.extend({
			defaults: {
				type: 'survey-text'
			}
		});
		
		var XABBlock = Backbone.Model.extend({
			defaults: {
				type: 'xab'
			}
		});		
		
		blockIdentifier.prototype.idAttribute = '_id';
		
		var Configuration = Backbone.Collection.extends({
			model : blockIdentifier(model, options)
			
		});
		
		var ConfigView = Backbone.View.extend({
			
			tagName: "ul",			
			className: "config",
			
			events: {
				
			},
			
		    render: function(){
		    	return this 
		    },
		    
		    initialize: function() {
		    	this.listenTo(Configuration, "change", this.render);	
		    }
			
		})
		
	})();

	
	
	
	

