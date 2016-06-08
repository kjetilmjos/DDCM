//var models = require('./models/schemas');
module.exports = function(app) {


  // normal routes ===============================================================
  // show the home page (will also have our login links)
  app.get('/', function(req, res) {
    res.render('index.ejs');
  });
}
