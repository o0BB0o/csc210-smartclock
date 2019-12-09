
        function format(time) {
            return moment(time).toString();
        }
        var table = $("#timesheets_table");

        // load timesheets with AJAX
        api_url = window.origin + "/api/v1/timesheets";

        var myArray = ['bg-primary', 'bg-secondary', 'bg-success','bg-danger','bg-warning','bg-info','bg-dark'];


        $.getJSON(api_url, function (response) {

            console.log(JSON.stringify(response));
            let timesheets = response;
            var k = 1;

            if (!($.isEmptyObject(timesheets))) {

                for (let ts of timesheets) {

                 ts_list_item = '<p class="list-group-item text-center text-white"> clock in time: ' +
                    format(ts.clock_in_time) + '<br> clock out time: ' + format(ts.clock_out_time) + '<br> date: ' + format(ts.date) + '</p>';

                 table.append(ts_list_item);

                }
                $('#timesheets_table .list-group-item').each(function () {
                    $(this).addClass(myArray[Math.floor(Math.random() * myArray.length)]);
                    $(this).prepend(k.toString() + '. ');
                    k++;
                });

            }

        });
