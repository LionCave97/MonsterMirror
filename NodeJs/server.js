var fs = require('fs')


function startUp(){
    console.log("Start up");


}

var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(8080, function(){
    console.log('Server running on 8080...');
});


startUp();