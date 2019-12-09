function updateTime() {
            $('#dayname').html(moment().format('dddd').toString());
            $('#dateinfo').html(moment().format('MMMM D YYYY').toString());
            $('#timeinfo').html(moment().format('h:mm:ss a').toString());
            setTimeout(updateTime, 1000);
        }
updateTime();
