import { MetadataService } from "@aws-sdk/ec2-metadata-service";
import * as http from 'http';

const host = '0.0.0.0';
const port = 5004;
const metadataService = new MetadataService({});
const token = await metadataService.fetchMetadataToken(); // fetches token explicitly
const instanceId = await metadataService.request("/latest/meta-data/instance-id", {});
const instanceType = await metadataService.request("/latest/meta-data/instance-type", {});
const az = await metadataService.request("/latest/meta-data/placement/availability-zone", {});

const requestListener = function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write("<html><body><h1>Graviton University Nodejs Demo</h1>");
    res.write("Instance ID: " + instanceId + "<br>");
    res.write("Instance Type: " + instanceType + "<br>");
    res.write("Instance AZ: " + az + "<br>");
    res.write("Node.js runtime: " + process.version + "<br>");
    res.write("</body></html>");
    res.end("");
};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
