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
            var csrftoken = getCookie('csrftoken')
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
            var csrftoken = getCookie('csrftoken')
            var url = '/dogpark/accept_request/';
            $('#'+elm.id).click(function() {
                console.log("clicked");
                var uname = $(this).attr('data-uname');
                console.log("username " + uname);
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrftoken,
                        uname: uname
                    },
                    success: function(json) {
                        console.log(json.response);
                        if(json.response == 1) {
                            console.log(json.response);
                            console.log(elm.id);
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
});