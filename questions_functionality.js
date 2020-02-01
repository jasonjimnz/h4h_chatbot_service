    //var BASE_URL = 'http://localhost:5000';
    var BASE_URL = 'http://159.122.82.189:5000';
    function check_event(eventName) {
        $.ajax({
            url: BASE_URL + '/trigger/' + eventName,
            success: function (response) {
                var query = prompt(response.question);
                $.ajax({
                    url: BASE_URL + '/talk',
                    method: 'POST',
                    data: {
                        'text': query
                    },
                    success: function (res) {
                        window.alert(res.response);
                        $('div.h4h_messages').append($('<div>').addClass('h4h_message_bot').text(res.response))
                    }
                });
            }
        });
    }

    $(document).ready(function () {
        //check_event('location_trigger');
        if ($('input.h4h_input_text').val() === '')
            return false;
        $.ajax({
            url: BASE_URL+'/chatbox',
            success: function (response) {
                $('body').append(response);
                check_event('ela_question_1');
            }
        });
        $('button.h4h_send_button').click(function(){
            $('div.h4h_messages').append($('<div>').addClass('h4h_message_user').text($('input.h4h_input_text').val()))
            $.ajax({
                    url: BASE_URL + '/talk',
                    method: 'POST',
                    data: {
                        'text': $('input.h4h_input_text').val()
                    },
                    success: function (res) {
                        $('div.h4h_messages').append($('<div>').addClass('h4h_message_bot').text(res.response))
                        $('input.h4h_input_text').val('')
                    }
                });
        })
    });