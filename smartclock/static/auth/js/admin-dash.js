/**
 *  - Header -
 *
 *
**/

function updateTime() {
            $('#dayname').html(moment().format('dddd').toString());
            $('#dateinfo').html(moment().format('MMMM D YYYY').toString());
            $('#timeinfo').html(moment().format('h:mm:ss a').toString());
            setTimeout(updateTime, 1000);
        }
updateTime();

/**
 *  - Main -
 *
 *
**/

$(document).ready(function(){
    fetch_data();
    function fetch_data()
    {
      $('#ajax_get_users_all').html({

        'url': '{{ url_for("get_timesheets") }}'



      })
    }


}





