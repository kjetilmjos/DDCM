//var models = require('./models/schemas');
module.exports = function(app) {


    var multer = require('multer');
    var upload = multer({
        dest: 'upload/'
    });
    var storage = multer.diskStorage({
        destination: function(req, file, cb) {
            cb(null, 'upload/')
        },
        filename: function(req, file, cb) {
            cb(null, "excel_export" + '.xlsx') //Appending .xlsx
        }
    })

    var upload = multer({
        storage: storage
    });
    // normal routes ===============================================================
    // show the home page (will also have our login links)
    app.get('/', function(req, res) {
        res.render('index.ejs');
    });

    app.post('/data-export', upload.single('up_file'), function(req, res) {
        // req.file is the `avatar` file
        // req.body will hold the text fields, if there were any
        console.log(req.file); //form files
        var PythonShell = require('python-shell');
        var pyshell = new PythonShell('file_validation.py');
        pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
});

// end the input stream and allow the process to exit
pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});

    })
}
