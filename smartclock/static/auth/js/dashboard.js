btnStartShift = $("#offline");
btnEndShift =  $("#online");
get_username = $("#username").text();
username = get_username.trim();
var alwaysGetsUpdated = "";

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

        var cancelAnimationFrame = window.cancelAnimationFrame ||
                window.webkitCancelAnimationFrame ||
                window.mozCancelAnimationFrame ||
                window.oCancelAnimationFrame ||
                window.msCancelAnimationFrame || function (callback) {
                    window.clearTimeout(callback);
                };

        var myReq;

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
        alwaysGetsUpdated = face.innerText;

        myReq = requestAnimationFrame(tick);
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
var apiUrl =  window.origin + "/api/v1/clock_status/" + username;
api_url = String(apiUrl);
$.getJSON(api_url, function (response) {
    let status = response;
    if (status.clock_status === true) {
        btnStartShift.hide();
        btnEndShift.show();
        lets_count(let_it_be_time = new Date(status.last_time));
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
                lets_count(let_it_be_time = new Date());
                message_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a');
                alert(message_time);
                $("#time").removeClass('bg-danger p-1 text-dark');
            } else {
                btnStartShift.show();
                btnEndShift.hide();
                lets_count(let_it_be_time = new Date());
                start_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a')+"\n";
                end_time = "ended at "+moment(data.clock_out_time).format('MMMM Do YYYY, h:mm:ss a');
                message_time = start_time + end_time;
                alert(message_time);

                var text = $("#time").text();
                var divClone = $("#time").clone();
                $("#time").replaceWith(divClone);
                get_time = getStamp(start=data.clock_in_time, end=data.clock_out_time);
                console.log(get_time);
                $("#time").text(get_time);
                $("#time").addClass('bg-danger p-1 text-dark');
            }
        })
    } else {
			alert('Alright!');
		}
})


function getStamp(start, end) {
    function paddy(num) {
        // adds leading zeros
        var pad_char = '0';
        var padlen = 2;
        var pad = new Array(1 + padlen).join(pad_char);
        return (pad + num).slice(-pad.length);
    }

    // start time and end time
    var t = "";

    var start = moment(start);
    var end = moment(end);

    // calculate total duration
    var duration = moment.duration(end.diff(start));

    // duration in hours
    var hours = parseInt(duration.asHours());

    if (hours !== 0) {
        t = t + String(paddy(hours)) + ':';
    } else {
        t = t + '00' + ':';
    }

    // duration in minutes
    var minutes = parseInt(duration.asMinutes())%60;
    if (minutes !== 0) {
        t = t + String(paddy(minutes)) + ':';
    } else {
        t = t + '00' + ':';
    }

    // duration in seconds
    var seconds = parseInt(duration.asSeconds())%60;
    if (seconds !== 0) {
        t = t + String(paddy(seconds));
    } else {
        t = t + '00';
    }
    return t
}