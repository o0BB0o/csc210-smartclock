/**
 *  - Sidebar -
 *
 *
**/

var flag = true;
if (flag == true) {
        $('#ibtn').attr('class', 'fas fa-angle-right fa-lg');
        flag = false;
    } else {
        $('#ibtn').attr('class', 'fas fa-angle-left fa-lg');
        flag=true;
}
$(document).ready(function () {
$("#sidebar").mCustomScrollbar({
    theme: "minimal"
});
$('#sidebarCollapse').on('click', function () {
    $('#sidebar, #content').toggleClass('active');
    $('.collapse.in').toggleClass('in');
    $('a[aria-expanded=true]').attr('aria-expanded', 'false');

    if (flag == true) {
        $('#ibtn').attr('class', 'fas fa-angle-right fa-lg');
        flag = false;
    } else {
        $('#ibtn').attr('class', 'fas fa-angle-left fa-lg');
        flag=true;
    }

});
});