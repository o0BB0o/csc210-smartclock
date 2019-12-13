btnStartShift = $("#offline");
btnEndShift =  $("#online");
get_username = $("#username").text();
username = get_username.trim();

function lets_count(let_it_be_time) {
	var defaults = {},
		one_second = 1000,
		one_minute = one_second * 60,
		one_hour = one_minute * 60,
		one_day = one_hour * 24,
		startDate = let_it_be_time,
		face = document.getElementById('time');

	var requestAnimationFrame = (function () {
		return window.requestAnimationFrame ||
			window.webkitRequestAnimationFrame ||
			window.mozRequestAnimationFrame ||
			window.oRequestAnimationFrame ||
			window.msRequestAnimationFrame ||
			function (callback) {
				window.setTimeout(callback, 1000 / 60);
			};
	}());

	tick();

	function tick() {

		var now = new Date(),
			elapsed = now - startDate,
			parts = [];

		parts[0] = '' + Math.floor(elapsed / one_hour);
		parts[1] = '' + Math.floor((elapsed % one_hour) / one_minute);
		parts[2] = '' + Math.floor(((elapsed % one_hour) % one_minute) / one_second);

		parts[0] = (parts[0].length == 1) ? '0' + parts[0] : parts[0];
		parts[1] = (parts[1].length == 1) ? '0' + parts[1] : parts[1];
		parts[2] = (parts[2].length == 1) ? '0' + parts[2] : parts[2];

		face.innerText = parts.join(':');

		requestAnimationFrame(tick);

	}
}

function updateTime() {
            $('#dayname').html(moment().format('dddd').toString());
            $('#dateinfo').html(moment().format('MMMM D YYYY').toString());
            $('#timeinfo').html(moment().format('h:mm:ss a').toString());
            setTimeout(updateTime, 1000);
        }

updateTime();

// brings back the appropriate button when the user is clocked in
// TODO: timer needs to be implemented too!
var apiUrl =  window.origin + "/api/v1/clock_status/" + username;
api_url = String(apiUrl);
$.getJSON(api_url, function (response) {
    let status = response;
    if (status.clock_status === true) {
        btnStartShift.hide();
        btnEndShift.show();
    } else {
        btnStartShift.show();
        btnEndShift.hide();
    }
})

$('.switch').on('click', function () {
    var msg = "";
    if ($(this).attr('id') == 'offline') {
        msg = "Do you want to clock in?";
    } else {
        msg = "Do you want to clock out?";
    }
    if (confirm(msg)) {
    	let url = window.origin + "/api/v1/clock/" + username;
        casted_url = String(url);
        $.getJSON(casted_url, function (response) {
            let data = response;
            if (data.is_clocked_in === true) {
                btnStartShift.hide();
                btnEndShift.show();

                lets_count(new Date());
                message_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a');
                alert(message_time);
            } else {
                btnStartShift.show();
                btnEndShift.hide();

                start_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a')+"\n";
                end_time = "ended at "+moment(data.clock_out_time).format('MMMM Do YYYY, h:mm:ss a');
                message_time = start_time + end_time;
                alert(message_time);
            }
        })
    } else {
			alert('Alright!');
		}
})






//
//btn_offline_start_shift = $("#offline");
//btn_online_end_shift = $("#online");
//btn_offline_start_shift.hide();
//btn_online_end_shift.hide();
//username = $("#username").text();
//username = username.trim();
//
//function checkOnline() {
//    let url = window.origin + "/api/v1/clock/" + username;
//    casted_url = String(url);
//    $.ajax({
//        "url": casted_url,
//        "dataType": "json",
//        "contentType": "application/json",
//        "type": "GET"
//    })
//        .done(function (response) {
//            var data = response;
//            if (data.is_clocked_in == true) {
//                btn_offline_start_shift.hide();
//                btn_online_end_shift.show();
//                var online = true;
//            } else {
//                btn_offline_start_shift.hide();
//                btn_online_end_shift.show();
//                var online = false;
//                    }
//                })
//}
//checkOnline();
//stop_watch = $("#time");
//mess = $("#message");
//
//$('.switch').each(function () {
//	$(this).on('click', function () {
//	    if (online == false) {
//	        msg = "Do you want to clock in?";
//	    } else {
//	        msg = "Do you want to clock out?";
//
//	    }
//		if (confirm(msg)) {
//			let url = window.origin + "/api/v1/clock/" + username;
//            casted_url = String(url);
//            message_time = "";
//            $.ajax({
//                    "url": casted_url,
//                    "dataType": "json",
//                    "contentType": "application/json",
//                    "type": "GET"
//                })
//                .done(function (response) {
//                    var data = response;
//                    if (data.is_clocked_in == true&&online = true) {
//                        btn_offline_start_shift.hide();
//                        btn_online_end_shift.show();
//                        stop_watch.text(getStamp(start=data.clock_in_time, end=data.clock_out_time));
//                        letscount(new Date());
//                        message_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a');
////                        mess.text(message_time);
//                        alert(message_time);
//                    } else {
//                        online = false;
//                        btn_offline_start_shift.show();
//                        btn_online_end_shift.hide();
//                        // brings an alert box
//                        start_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a')+"\n";
//                        end_time = "ended at "+moment(data.clock_out_time).format('MMMM Do YYYY, h:mm:ss a');
//                        message_time = start_time + end_time;
////                        mess.html(message_time);
//                        alert(message_time);
//                    }
//                })
//                .fail(function (xhr, status, description) {
//                    alert("There was a problem handling this request");
//                    console.log("Error: " + description);
//                    console.log("Status: "+ status);
//                })
//                .always(function (xhr, status) {
//                    console.log("request completed with status code: " + status);
//                });
//		} else {
//			alert('Alright!');
//		}
//	});
//});
//

//
//
////
////function getStamp(start, end, al=false) {
////    // start time and end time
////    var t = "";
////    var text = "";
////
////    // calculate total duration
////    var duration = moment.duration(end.diff(start));
////
////    // duration in hours
////    var hours = parseInt(duration.asHours());
////
////    if (hours !== 0) {
////        t = t + hours + ':';
////        if (hours !== 1) {
////            text = text + hours + ' hour and ';
////        } else {
////            text = text + hours + ' hours and ';
////        }
////
////    }
////
////    // duration in minutes
////    var minutes = parseInt(duration.asMinutes())%60;
////    if (minutes !== 0) {
////        t = t + minutes + ':';
////        if (minutes !== 1) {
////            text = text + minutes + ' minute and ';
////        } else {
////            text = text + minutes + ' minutes and ';
////        }
////
////    }
////
////    // duration in seconds
////    var seconds = parseInt(duration.asSeconds())%60;
////    if (seconds !== 0) {
////        t = t + seconds;
////        if (seconds !== 1) {
////            text = text + seconds + ' second.';
////        } else {
////            text = text + seconds + ' seconds.';
////        }
////    }
////
////    if (al===true){
////        text = "Today you have worked " + text + "\nfrom " + "moment(start).format('h:mm a') " + "to " + "moment(end).format('h:mm a')";
////        return text;
////    } else {
////        return t;
////    }
////}
////
////function add_a_second() {
////
////    btn_out.val
////}
////
////if ($("#online").is(":visible")) {
////
////}