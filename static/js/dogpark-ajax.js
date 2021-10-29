$(document).ready(function() {
    const url = "dogregisterform/";
    /* Select num dogs to be just one */
    var num_dogs = 1;
    var i;
    
        $("select#id_num_dogs").change(function(){
            num_dogs = $(":selected").text();
            num_dogs = num_dogs.match(/\d/);
            num_dogs = parseInt(num_dogs[0]);
            var elm = $("#prof");
            var content = null;

            fetch(url)
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                elm.empty();
                for(i = 0; i < num_dogs; i++) {
                    elm.append(data.form);
                }
            });  
        });

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
                            $('#successful_request'+elm.id.match(/\d+$/)).show();
                            $("#"+elm.id).hide();
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status+": "+xhr.responseText);
                    }
                });
            })
        }
        
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
                            $('#friends'+elm.id.match(/\d+$/)).show();
                            $("#"+elm.id).hide();
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status+": "+xhr.responseText);
                    }
                });
            })
        }

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
                            $('#decline_event'+elm.id.match(/\d+$/)).show();
                            $('#attending_event'+elm.id.match(/\d+$/)).show();  
                            $(elmId).hide();
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status+ ": "+xhr.responseText);
                    }
                });
            });
        }

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

        var buttons = $("#people_list").find('button')
        buttons.each(function(index, elm) {
            if(elm.id.startsWith("add_friend_btn")) {
                sendFriendRequest(elm);
            }
        });

        buttons = $("#friend_request_list").find('button')
        buttons.each(function(index, elm) {
            if(elm.id.startsWith("accept_friend_btn")) {
                acceptFriendRequest(elm);
            }
        });

        buttons = $('#Events').find('button')
        buttons.each(function(index, elm) {
            if(elm.id.startsWith("attend_event")) {
                attendEvent(elm);
            }
            else if(elm.id.startsWith("decline_event")) {
                declineEvent(elm);
            }
        });

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
        })
});