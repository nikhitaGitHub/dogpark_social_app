/**
 * On document ready, bind events to buttons and select tag
 */

$(document).ready(function() { 
    //Fetch from this URL
    const url = "dogregisterform/";
    /* Select num dogs to be just one */
    var num_dogs = 1;
    var i;
    //Bind change listener, when user selects a different value from dropdown for number of dogs
    $("select#id_num_dogs").change(function(){
        num_dogs = $(":selected").text();
        //Extract the number value of dogs
        num_dogs = num_dogs.match(/\d/);
        num_dogs = parseInt(num_dogs[0]);
        var elm = $("#prof");
        var i = 0;
        var content = null;
        //Send a get request 
        fetch(url+num_dogs+'/')
        //Return the received form for each dog 
        .then(function(response) {
            return response.json();
        })
        //On receiveing form , render on the UI
        .then(function(data) {
            elm.empty();
            elm.append(data.form);
        });
        //This is crispy form or formset factory attribute not setting this will cause trouble
        $('#id_form-TOTAL_FORMS').val(num_dogs);
    });

    //For CSRF token 
    function getCookie(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie != "") {
            var cookies = document.cookie.split(';');
            for(i=0; i<cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if(cookie.substring(0, name.length+1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //Funtion to POST a friend request to the DB
    function sendFriendRequest(elm) {
        var csrftoken = getCookie('csrftoken');
        var url = '/dogpark/send_friend_request/';

        $('#'+elm.id).click(function() {
            var uname = $(this).attr('data-uname');
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    uname: uname
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#successful_request'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $('#confirm'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $("#"+elm.id).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+": "+xhr.responseText);
                }
            });
        })
    }

    //Function to POST acceptance of friend request to DB
    function acceptFriendRequest(elm) {
        var csrftoken = getCookie('csrftoken');
        var url = '/dogpark/accept_request/';
        $('#'+elm.id).click(function() {
            var uname = $(this).attr('data-uname');
            $.ajax({
                url: url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    uname: uname
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#friends'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $('#confirm'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $("#"+elm.id).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+": "+xhr.responseText);
                }
            });
        })
    }

    //Function to POST a event as attending to DB
    function attendEvent(elm) {
        var elmId = '#'+elm.id;
        var url = '/dogpark/attend_event/';
        var csrftoken = getCookie('csrftoken');
        $(elmId).click(function() {
            var eventid = $(this).attr('data-elmid');
            $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    eventid: eventid
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#decline_event'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $('#attending_event'+elm.id.match(/\d+$/)).css('display', 'inline-block');
                        $('#confirm'+elm.id.match(/\d+$/)).css('display', 'inline-block'); 
                        $(elmId).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText);
                }
            });
        });
    }

    //Function to decline an event and delete form DB
    function declineEvent(elm) {
        var elmId = '#'+elm.id; 
        var url = '/dogpark/decline_event/';
        var csrftoken = getCookie('csrftoken');
        $(elmId).click(function() {
            var eventid = $(this).attr('data-elmid');
            $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    eventid: eventid
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#attending_event'+elm.id.match(/\d+$/)).hide();
                        $('#confirm'+elm.id.match(/\d+$/)).hide();
                        $('#attend_event'+elm.id.match(/\d+$/)).show();
                        $(elmId).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            });
        });
    }

    //Function to POST a goal into MyGoal table
    function addGoal(elm) {
        var elmId = '#'+elm.id; 
        var url = '/dogpark/add_goal/';
        var csrftoken = getCookie('csrftoken');
        $(elmId).click(function() {
            var goalid = $(this).attr('data-goalid');
            $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    goalid: goalid
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#finish_goal'+elm.id.match(/\d+$/)).show();
                        $('#remove_goal'+elm.id.match(/\d+$/)).show();
                        $(elmId).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            });
        });
    }

    //Function to mark a goal finsished and add to achievements
    function finishGoal(elm) {
        var elmId = '#'+elm.id; 
        var url = '/dogpark/finish_goal/';
        var csrftoken = getCookie('csrftoken');
        $(elmId).click(function() {
            var goalid = $(this).attr('data-goalid');
            $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    goalid: goalid
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#goal_completed'+elm.id.match(/\d+$/)).show();
                        $('#remove_goal'+elm.id.match(/\d+$/)).hide();
                        $(elmId).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            });
        });
    }

    //Function to remove a goal from DB
    function removeGoal(elm) {
        var elmId = '#'+elm.id; 
        var url = '/dogpark/remove_goal/';
        var csrftoken = getCookie('csrftoken');
        $(elmId).click(function() {
            var goalid = $(this).attr('data-goalid');
            $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken,
                    goalid: goalid
                },
                success: function(json) {
                    if(json.response == 1) {
                        $('#finish_goal'+elm.id.match(/\d+$/)).hide();
                        $('#add_goal'+elm.id.match(/\d+$/)).show();
                        $(elmId).hide();
                    }
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            });
        });
    }

    //Find all Add freind buttons for each user and invoke function for each
    var buttons = $("#people_list").find('button')
    buttons.each(function(index, elm) {
        if(elm.id.startsWith("add_friend_btn")) {
            sendFriendRequest(elm);
        }
    });

    //Find all Accept freind buttons for each user and invoke funtion for each
    buttons = $("#friend_request_list").find('button')
    buttons.each(function(index, elm) {
        if(elm.id.startsWith("accept_friend_btn")) {
            acceptFriendRequest(elm);
        }
    });

    //Find all Attend buttons for each event and invoke funtion for each
    buttons = $('#Events').find('button')
    buttons.each(function(index, elm) {
        if(elm.id.startsWith("attend_event")) {
            attendEvent(elm);
        }
        else if(elm.id.startsWith("decline_event")) {
            declineEvent(elm);
        }
    });

    //Find all Add Goal buttons for each goal and invoke funtion for each
    buttons = $('#Goals').find('button')
    buttons.each(function(index,elm) {
        if(elm.id.startsWith("add_goal")) {
            addGoal(elm);
        }
        else if(elm.id.startsWith("finish_goal")) {
            finishGoal(elm);
        }
        else if(elm.id.startsWith("remove_goal")) {
            removeGoal(elm);
        }
    });

    //On button click , POST to check in url to check in a user to park in DB
    $("#checkIn").click(function(index, elm) {
        var url = '/dogpark/check_in/';
        var csrftoken = getCookie('csrftoken');
        $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(json) {
                        $('#checkOut').show();
                        $('#checkIn').hide();
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            });
    });

    //Store user rating upon selecting one of the 5 ratings
    $("input[type=radio]").click(function(){
        var url= '/dogpark/rating/';
        var csrftoken = getCookie('csrftoken');
        var rating = $("input[type='radio']:checked").val();
        $.ajax({
            url:url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
                rating: rating
            },
            success: function(json) {

            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status+ ": "+xhr.responseText)
            }
        });
    });

    //On button click , POST to check out url to check out a user out of the park in DB
    $("#checkOut").click(function(index, elm) {
        var url = '/dogpark/check_out/';
        var csrftoken = getCookie('csrftoken');
        $.ajax({
                url:url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(json) {
                        $('#checkIn').show();
                        $('#checkOut').hide();
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status+ ": "+xhr.responseText)
                }
            }); 
    });
    //Repeated code from above 
    $("#checkIn").click(function(index, elm) {
            var url = '/dogpark/check_in/';
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                    url:url,
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrftoken
                    },
                    success: function(json) {
                            $('#checkOut').show();
                            $('#checkIn').hide();
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status+ ": "+xhr.responseText)
                    }
                });
        });
});
