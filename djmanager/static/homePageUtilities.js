$(function () {
    function get_lang(french, english) {
        if (document.documentElement.lang === 'fr') {
            return french;
        }
        else if (document.documentElement.lang === 'en') {
            return english;
        }
        else {
            throw "Unsupported language!";
        }
    }

    $('#registrationWrapper').hide();
    $('form.login a').click(function () {
        $('#registrationWrapper').slideDown();
    });




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

    $("#logoutButton").click(function (evt) {
        evt.preventDefault();
        var logoutForm = document.getElementById('logoutElements');
        logoutForm.style.display = 'none';
        logoutForm.removeChild(logoutForm.childNodes[0]);

        $.ajax({
            url: 'cgi-bin/logout.php',
            success: function () {
                $("fieldset#loginElements").css("display", "block");
                document.getElementById('loginButton').disabled = false;
                document.getElementById('loginButton').innerHTML = get_lang("Connexion", "Login");
                $("#login").attr("data-logged", "no");
                delete_cookie("catExperimentLogin");
            }
        });
    });

    $("#registration").validate({
        rules: {
            username: {
                required: true,
                rangelength: [2, 16],
                remote: './cgi-bin/checkUsr.php'
            },

            password: {
                required: true,
                rangelength: [8, 16]
            },

            passwordRepeat: {
                equalTo: '#registration input[name=password]'
            },

            email: {
                required: true,
                email: true,
                remote: './cgi-bin/checkEmail.php'
            }
        },
        messages: {
            username: {
                required: get_lang("Veuillez fournir un identifiant", "Please provide an identifier"),
                rangelength: get_lang("Votre pseudonyme doit faire entre 2 et 16 caractères", "Your username must have 2 to 16 characters"),
                remote: get_lang("Ce nom d'usager est déjà pris!", "This username is already in use")
            },

            password: {
                required: get_lang("Veuillez fournir un mot de passe", "Please provide a password"),
                rangelength: get_lang("Votre mot de passe doit avoir de 8 à 16 caractères", "Password must have between 8 and 16 characters")
            },

            passwordRepeat: {
                required: get_lang("Veuillez répéter votre mot de passe", "Please confirm your password"),
                equalTo: get_lang("Votre confirmation ne correspond pas au mot de passe", "Confirmation does not match")
            },

            email: {
                required: get_lang("Veuillez fournir une adresse courriel", "Please provide an email adress"),
                email: get_lang("Cette adresse n'est pas valide", "This address is not valid"),
                remote: get_lang("Cette adresse est déjà enregistrée avec nous", "This email adress is already registered")
            }
        },
        submitHandler: function (form) {
            theButton = form.getElementsByTagName("button")[0];
            theButton.disabled = true;
            theButton.innerHTML = "<img src='style/ajax-loader.gif' />";
            form.action = "cgi-bin/register.php";
            form.method = "POST";
            form.submit();
        }
    });

    $("#proceed").click(function (evt) {
        evt.preventDefault();
        //i guess we should technically make a server request to see if we're logged in...
        //we could look for client side signs but that's very not much secure
        $("#username").focus();
        $(this).attr("disabled", true);
        if ($("#login").attr("data-logged") === "yes") {
            window.location.replace("Experiment.php");
        }
        else {

            var advice = $("<div id='advice' style='width:0px; height:60px'>" + get_lang("veuillez vous authentifier ou créer un compte si vous n'en avez pas!", "Please login or create an account if you do not have one!") + "</div>", {
                "id": "advice",
                "width": 0
            });

            $("#login").prepend(advice);

            advice.animate({ width: "200px" }, 200);

            setTimeout(function () {
                advice.hide();
                $("#proceed").attr("disabled", false);
            }, 4000);
        }


    })
});