//var models = require('./models/schemas');
module.exports = function(app) {


    var multer = require('multer');
    //    var upload = multer({
    //      dest: 'upload/'
    //  });
    var storage = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, 'upload/')
        },
        filename: function(req, file, cb) {
            cb(null, "excel_export" + '.xlsx') //Appending .xlsx
        }
    })
    var storage_config = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, 'upload/')
        },
        filename: function(req, file, cb) {
            cb(null, "CONFIG_query" + '.json') //Appending .json
        }
    })

    var upload = multer({
        storage: storage
    });
    var upload_config = multer({
        storage: storage_config
    });
    // normal routes ===============================================================
    // show the home page (will also have our login links)
    app.get('/', function(req, res) {

        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/dates_query.py');
        var mssg = [];
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)

            mssg = message.split(",");
        
        });

        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.render('index.ejs', {
                'allowed_dates': mssg
            });
        });

    });

    app.post('/data-export', upload.single('up_file'), function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any
        console.log(req.file); //form files
        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/file_validation.py');
        var mssg = "";
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            mssg = message;
        });

        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.send(mssg);
        });

    });
    app.post('/config_upload', upload_config.single('config_file'), function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any
        console.log(req.file); //form files
        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/mongodb_query.py');
        var msg = "";
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            msg = message;
        });
        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.send(msg);
        });


    });

    app.post('/cleanup_files', function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any

        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/cleanup.py');
        var msgg = "";
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            msgg = message;
        });
        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.send(msgg);
        });


    });
    app.post('/generate_csv', function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any

        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/PN1042_parser.py');
        var msgg = "";
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            msgg = message;
        });
        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.send(msgg);
        });


    });
    app.post('/store_data', function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any

        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('./python/mongodb_datapusher.py');
        var msgg = "";
        pyshell.on('message', function(message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log(message);
            msgg = message;
        });
        // end the input stream and allow the process to exit
        pyshell.end(function(err) {
            if (err) throw err;
            console.log('finished');
            res.send(msgg);
        });


    })
}
