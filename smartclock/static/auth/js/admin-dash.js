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
 *  - REST API Get Method -
 *
 *
 **/

var table = $("#users_table");

table.append('<div id = "first" class="list-group"></div>');
table.append('<div id = "second" class="list-group"></div>');

// load users with AJAX
api_url = window.origin + "/api/v1/users"

$.getJSON(api_url, function (response) {

    let users = response[0];
    var k = 1;

    if (!($.isEmptyObject(users))) {

        for (let user of users) {

            if ( user.is_admin === false ) {
                 user_list_item = '<a class="list-group-item list-group-item-action" href="' + window.origin +
                    '/assign/' + user.username + '">' +
                    user.first_name + ' ' + user.last_name + ' - username: ' + user.username +
                    '<i class="fas fa-user-edit" style="float:right"></i></a>';

//              console.log(user_list_item);
                if (user.is_approved) {
                    $("#first").append(user_list_item);
                } else {
                    $("#second").append(user_list_item);
                }

            }
        }

        if ($('#first').html() != '') {
            $("#first").prepend("<p>Approved Users</p>");
        }

        if ($('#second').html() != '') {
            $("#second").prepend("<p class='pt-4'> Waiting to be Approved</p>");
        }

        $('#content .list-group-item-action').each(function () {
            $(this).prepend(k.toString() + '. ');
            k++;
        });

    }

});
