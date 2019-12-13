btnStartShift = $("#offline");
btnEndShift =  $("#online");
get_username = $("#username").text();
username = get_username.trim();

function lets_count(let_it_be_time, stop) {

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
        var cancelAnimationFrame = window.cancelAnimationFrame || window.mozCancelAnimationFrame;
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

        myReq = requestAnimationFrame(tick);

        if(stop === true){
            cancelAnimationFrame(myReq);
        }
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
        lets_count(let_it_be_time = new Date(status.last_time), stop = false);
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
                lets_count(let_it_be_time = new Date(), stop=false);
                message_time = "started at "+moment(data.clock_in_time).format('MMMM Do YYYY, h:mm:ss a');
                alert(message_time);
            } else {
                btnStartShift.show();
                btnEndShift.hide();
                lets_count(let_it_be_time = new Date(), stop=true);
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