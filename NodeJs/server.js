var https = require('https'); //Https module of Node.js
var fs = require('fs'); //FileSystem module of Node.js
var FormData = require('form-data'); //Pretty multipart form maker.
var folder = "../pics";

var ACCESS_TOKEN = "";

function Facebook(){
    console.log("Start up");

    if (fs.existsSync(folder)){
      fs.readdir(folder, (err, files) => {
        files.forEach(file => {
          console.log(file);

          var form = new FormData(); //Create multipart form
          form.append('file', fs.createReadStream(folder+'/'+file)); //Put file
          form.append('message', "The Real Monster"); //Put message
          
          //POST request options, notice 'path' has access_token parameter
          var options = {
              method: 'post',
              host: 'graph.facebook.com',
              path: '/me/photos?access_token='+ACCESS_TOKEN,
              headers: form.getHeaders(),
          }
          
          //Do POST request, callback for response
          var request = https.request(options, function (res){
              console.log(res);
          });
          
          //Binds form to request
          form.pipe(request);
          
          //If anything goes wrong (request-wise not FB)
          request.on('error', function (error) {
              console.log(error);
          });


        });
      });
    }

}

function CopyPics(){

  if (fs.existsSync(folder)){
    fs.readdir(folder, (err, files) => {
      files.forEach(file => {
        console.log(file);

        var cbCalled = false;

        var rd = fs.createReadStream(folder + "/" +file);
        rd.on("error", function(err) {
        });
        var wr = fs.createWriteStream("./pics/" + file);
        wr.on("error", function(err) {
        });
        wr.on("close", function(ex) {
        });
        rd.pipe(wr);        
        


      });
    });
  }

}

var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(8080, function(){
    console.log('Server running on 8080...');
});


CopyPics();
Facebook();

 
