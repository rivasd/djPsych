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
    			$("#login-error").text(resp.responseJSON.form_errors.__all__[0])
    		}
    	})
    });
    
    var $signinbutton = $("#sign-in-popup");
    
    if($signinbutton.length){
    	$signinbutton.click(function(evt){
    		evt.preventDefault();
    		$("#hidden-login").dialog({
    			modal: true,
    			dialogClass: 'login-popup',
    			draggable: false,
    			height: 'auto',
    			resizable: false,
    			width: 400,
    			appendTo: "#content"
    		})
    		
    	});
    }
    
    function delete_cookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
});