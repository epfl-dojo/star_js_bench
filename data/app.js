var fs = require('fs'),
    http = require('http');

function respond(res, err, data) {
    if (err) {
        res.writeHead(404);
        res.end(JSON.stringify(err));
        return;
    }
    res.writeHead(200);
    res.end(data);
}

http.createServer(function (req, res) {
    if (req.url.endsWith("jsonp")) {
        var jsonFile = req.url.replace(/p$/, "");
        fs.readFile(__dirname + jsonFile, function(err, data) {
            respond(res, err, "p = " + data);
        });
    } else {
        fs.readFile(__dirname + req.url, function(err, data) {
            respond(res, err, data);
        });
    }
}).listen(8000);