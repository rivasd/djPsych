$(function () {
    //Add the toggle functionality to jQuery
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

    
    
    var $signinbutton = $("#sign-in-popup");
    
    
    
    var dialog = document.getElementById("hidden-login");
    if (! dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    
    dialog.querySelector(".close").addEventListener('click', function(){
    	dialog.close();
    });
    
    
    if($signinbutton.length){
    	$signinbutton.click(function(evt){
    		evt.preventDefault();
    		dialog.show();
    	});
    }
    
    $("#hidden-login-form").submit(function (evt) {
    	evt.preventDefault()
    	$.ajax({
    		method: 'POST',
    		url: '/accounts/login/',
    		data: $(this).serialize(),
    		success: function(resp){
    			window.location.reload();
    		},
    		error: function(resp){
    			if(resp.responseJSON.form_errors.__all__){
    				$("#login-error").text(resp.responseJSON.form_errors.__all__[0]).css('visibility', 'visible');
    			}
    			else{
    				['login', 'password'].forEach(function(elem){
    					if(resp.responseJSON.form_errors[elem]){
    						$("#mdl-dialog__"+elem+"-error").text(resp.responseJSON.form_errors[elem]).css('visibility', 'visible');
    					}
    				});
    			}
    		}
    	})
    });
    
    
    function delete_cookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
});