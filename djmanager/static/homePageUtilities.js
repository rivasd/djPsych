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

    //Little hack to allow hovering back and forth to original color, whichever it is (god what would we do w/out StackOverflow)
    var originalColors = [];

    $('a').each(function () {
        originalColors[$(this).index('a')] = $(this).css('color');
        $(this).hover(function () {
            $(this).stop().animate({
                'color': '#ec4409'
            }, 250);
        }, function () {
            $(this).stop().animate({
                'color': originalColors[$(this).index('a')]
            }, 250);
        });
    });
    /*
    document.getElementById('login').onsubmit = function (evt) {
    evt.preventDefault();
    var theButton = this.getElementsByTagName('button')[0];
    theButton.disabled = true;
    theButton.innerHTML = '<img src="style/ajax-loader.gif" />';
    this.action = "cgi-bin/Login.php";
    this.method = "POST";
    this.submit();
    }
    */

    //will store the login form (inside a jQuery object) so that we can recreate it easily after a user logs out
    var originalForm;

    $("#login").submit(function (evt) {
        evt.preventDefault();
        originalForm = $(this);
        var elem = this;
        $(this).find("button[type=submit]").attr('disabled', true).html('<img src="style/ajax-loader.gif" />');
        $.ajax({
            url: "cgi-bin/Login.php",
            method: 'post',
            data: {
                username: elem.username.value,
                password: elem.password.value
            },
            success: function (answer) {
                answer = JSON.parse(answer);
                console.log(answer);
                if (answer[0] === true) {
                    $("fieldset#loginElements").css("display", "none");
                    $("fieldset#logoutElements").css("display", "block");
                    $("#greeting").html(get_lang("Bonjour, ", "Welcome, ") + answer[1] + "!");
                    $("#login").attr("data-logged", "yes");
                }
                else {
                    elem.getElementsByTagName("button")[0].innerHTML = get_lang("Réessayer", "Try Again");
                    elem.getElementsByTagName("button")[0].disabled = false;
                    alert(answer[1]);
                }
            }
        });
    });

    function delete_cookie(name) {
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
});