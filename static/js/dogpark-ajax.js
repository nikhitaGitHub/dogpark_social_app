$(document).ready(function() {
    const url = "dogregisterform/";
    /* Select num dogs to be just one */
    var num_dogs = 1;
    var i;
    
        $("select#id_num_dogs").change(function(){
            num_dogs = $(":selected").text();
            var elm = $("#prof");
            fetch(url)
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                elm.empty();
                for(i = 0; i <num_dogs; i=i+1) {
                    elm.append(data.form);
                }
            });
        });

        function getCookie(name) {
            var cookieValue = null;
            if(document.cookie && document.cookie != "") {
                var cookies = document.cookie.split(';');
                for(i=0; i<cookies.length; i=i+1) {
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
            var url1 = '/dogpark/send_friend_request/';
            var url2 = '/dogpark/accept_request'
            $('#'+elm.id).click(function() {
                console.log(uname)
                var uname = $(this).attr('data-uname');
                $.ajax({
                    url: url1,
                    type: "POST",
                    data: {
                        csrfmiddlewaretoken: csrftoken,
                        uname: uname
                    },
                    success: function(json) {
                        if(json.response === 1) {
                            var btn = $(this)
                            $('#accept_request'+elm.id.match(/\d+$/)).show();
                            btn.hide();
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
                sendFriendRequest(elm)
            }
        });
});