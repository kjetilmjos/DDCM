function RemoveFiles(){
  return $.ajax({
      url: '/cleanup_files',
      type: 'POST',
      data: "post",
      success: function(data) {
            alert(data);
      }
  });

}

function Generate_CSV(){
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

function Store_to_DB(){
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

function execute(){
alert(document.getElementById('start_date').value);

}


//function validate() {

  //  var fullPath = document.getElementById('excel_upload_file').value;
//    alert(fullPath);
//    if (fullPath) {
  //      var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
    //    var filename = fullPath.substring(startIndex);
      //  if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        //    filename = filename.substring(1);
        //}
        //alert(filename);
//    }






//}
