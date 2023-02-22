const http = require('http');
const metadata = require('node-ec2-metadata');
const Q = require('q');

const host = '0.0.0.0';
const port = 5004;

const requestListener = function (req, res) {
    Q.all([
        metadata.getMetadataForInstance('instance-id'),
        metadata.getMetadataForInstance('instance-type'),
        metadata.getMetadataForInstance('placement/availability-zone'),
    ])
    .spread(function(instanceId, instanceType, az) {
        res.writeHead(200, {'Content-Type': 'text/html'});
        res.write("<html><body><h1>Graviton University Nodejs Demo</h1>");
        res.write("Instance ID: " + instanceId + "<br>");
        res.write("Instance Type: " + instanceType + "<br>");
        res.write("Instance AZ: " + az + "<br>");
        res.write("Node.js runtime: " + process.version + "<br>");
        res.write("</body></html>");
        res.end("");
    })

};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});

