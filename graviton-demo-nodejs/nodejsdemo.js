var http = require('http');


 
    response.writeHead(200, {'Content-Type': 'text/plain'});

    response.write("<html><body><h1>Graviton University Python Demo</h1>");
    response.write("</body></html>");
    response.end();
).listen(5000);

// 
console.log('Server running ...');
