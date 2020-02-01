    var BASE_URL = 'http://localhost:5000';

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
                    }
                });
            }
        });
    }

    $(document).ready(function () {
        check_event('location_trigger');
    });