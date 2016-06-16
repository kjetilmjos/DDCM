function RemoveFiles() {
    return $.ajax({
        url: '/cleanup_files',
        type: 'POST',
        data: "post",
        success: function(data) {
            alert(data);
        }
    });

}

function Generate_CSV() {
    document.getElementById('parse_status').innerHTML = "Parsing file, grab a coffee....";
    return $.ajax({
        url: '/generate_csv',
        type: 'POST',
        data: "post",
        success: function(data) {
            document.getElementById('parse_status').innerHTML = data;
        }
    });

}

function Store_to_DB() {
    document.getElementById('db_storage_status').innerHTML = "Storing data, 2sec....";
    return $.ajax({
        url: '/store_data',
        type: 'POST',
        data: "post",
        success: function(data) {
            document.getElementById('db_storage_status').innerHTML = data;
        }
    });

}

function generate_config() {
    document.getElementById('config_status').innerHTML = "Generating config file...."
    var start_date = document.getElementById('start_date').value;
    var end_date = document.getElementById('end_date').value;

    var a = moment(start_date, 'YYYY-MM-DD HH:MM:SS');
    var b = moment(end_date, 'YYYY-MM-DD HH:MM:SS');


    var itr = moment.twix(new Date(a), new Date(b)).iterate("days");

    var range = [];
    while (itr.hasNext()) {
        range.push(itr.next().toDate());

    }

    var arr = [];
    var len = range.length;
    for (var i = 0; i < len; i++) {
        arr.push({
            date: range[i]
        });
    }


    return $.ajax({
        url: '/generate_config',
        type: 'POST',
        data: {
            "dates": arr,
        },

        success: function(data) {
            document.getElementById('config_status').innerHTML = data;
        }
    });

}

function execute() {
  document.getElementById('query_status').innerHTML = "Searching DB...."
    return $.ajax({
        url: '/execute_query',
        type: 'POST',
        data: "post",
        success: function(data) {
            document.getElementById('query_status').innerHTML = data;
        }
    });

}
