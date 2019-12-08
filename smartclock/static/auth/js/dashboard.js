function updateTime() {
            $('#dayname').html(moment().format('dddd').toString());
            $('#dateinfo').html(moment().format('MMMM D YYYY').toString());
            $('#timeinfo').html(moment().format('h:mm:ss a').toString());
            setTimeout(updateTime, 1000);
        }
updateTime();

btn_in = $("#offline");
btn_out = $("#online");
username = $("#username").text();
username = username.trim();

btn_out.hide();

$('.switch').each(function () {
	$(this).on('click', function () {
	    val = $(this).attr('value');
        var msg = "";

	    if (val === "offline") {
	        msg = "Do you want to clock in?";
	    } else {
	        msg = "Do you want to clock out?";
	    }
		if (confirm(msg)) {
			let url = window.origin + "/api/v1/clock/" + username;
            casted_url = String(url); // I don't know what am I doing...
            data_json = { }
            $.ajax({
                    "url": casted_url,
                    "data": JSON.stringify(data_json),
                    "dataType": "json",
                    "contentType": "application/json",
                    "type": "PATCH"
                })
                .done(function (response) {
                    var data = response[0];

                    if (data.hasOwnProperty('error')){
                        alert(JSON.stringify(data));
                    } else {
                        if (data.is_clocked_in === true) {
                            btn_in.show();
                            btn_out.hide();
                            $('#timer').text=getStamp(start=data.clock_in_time, end=data.clock_out_time);
                        } else {
                            btn_out.show();
                            btn_in.hide();
                            // brings an alert box
                            getStamp(start=data.clock_in_time, end=data.clock_out_time, al=true);
                        }
                    }
                })
                .fail(function (xhr, status, description) {
                    alert("There was a problem handling this request");
                    console.log("Error: " + description);
                    console.log("Status: + status");
                })
                .always(function (xhr, status) {
                    console.log("request completed with status code: " + status);
                });
		} else {
			alert('Alright!');
		}
	});
});

function getStamp(start, end, al=false) {
    // start time and end time
    var startTime = start;
    var endTime = end;
    var t = "";
    var text = "";

    // calculate total duration
    var duration = moment.duration(endTime.diff(startTime));

    // duration in hours
    var hours = parseInt(duration.asHours());

    if (hours !== 0) {
        t = t + hours + ':';
        if (hours !== 1) {
            text = text + hours + ' hour and ';
        } else {
            text = text + hours + ' hours and ';
        }

    }

    // duration in minutes
    var minutes = parseInt(duration.asMinutes())%60;
    if (minutes !== 0) {
        t = t + minutes + ':';
        if (minutes !== 1) {
            text = text + minutes + ' minute and ';
        } else {
            text = text + minutes + ' minutes and ';
        }

    }

    // duration in seconds
    var seconds = parseInt(duration.asSeconds())%60;
    if (seconds !== 0) {
        t = t + seconds;
        if (seconds !== 1) {
            text = text + seconds + ' second.';
        } else {
            text = text + seconds + ' seconds.';
        }
    }

    if (al===true){
        text = "So far you have worked only " + text;
        alert(text);
    } else {
        return t;
    }
}
//
//function add_a_second() {
//
//    btn_out.val
//}
//
//if ($("#online").is(":visible")) {
//
//}