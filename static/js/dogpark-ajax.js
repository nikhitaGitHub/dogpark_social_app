$(document).ready(function() {
    const url = "dogregisterform/";
    /* Select num dogs to be just one */
    var num_dogs = 1;
    var i;
    
        $("select#id_num_dogs").change(function(){
            num_dogs = $(':selected').text();
            fetch(url)
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                for(i = 0; i <num_dogs; i++) {
                    $("#prof").append(data.form)
                }
            });
    })

    /*fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            for(i = 0; i <num_dogs; i++) {
                $("#prof").append(data.form);
            }
        });
    }*/
        function getCookie(name) {
            var cookieValue = null;
            if(document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for(var i=0; i<cookies.length; i++) {
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
            console.log("Sending request")
            $('#'+elm.id).click(function() {
                console.log(uname)
                var uname = $(this).attr('data-uname');
                $.ajax({
                    url: url,
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrftoken,
                        uname: uname
                    },
                    success: function(json) {
                        if(json.response === 1) {
                            $('#sent_friend_request'+elm.id.match(/\d+$/)).show();
                            $(this).hide();
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status+": "+xhr.responseText)
                    }
                });
            })
        }
        
        var buttons = $("#people_list").find('button')
        buttons.each(function(index, elm) {
            if(elm.id.startsWith("add_friend_btn")) {
                sendFriendRequest(elm)
            }
        });
})