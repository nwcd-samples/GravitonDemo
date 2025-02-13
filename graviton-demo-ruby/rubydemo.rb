require 'socket'
require 'uri'
require 'net/http'
require 'aws-sdk-core'

def getmetadata(url)
  uri = URI(url)
  res = Net::HTTP.get_response(uri)
  return res.body if res.is_a?(Net::HTTPSuccess)
end

begin
server = TCPServer.new '0.0.0.0' ,5001

puts 'Server is running on http://0.0.0.0:5001'

loop {                                                  
  Thread.start(server.accept) do | client |
  first_line = client.gets
  verb, path, _ = first_line.split

  if verb == 'GET'
      ec2_metadata = Aws::EC2Metadata.new
      instancetype = ec2_metadata.get('/latest/meta-data/instance-type')
      instanceid = ec2_metadata.get('/latest/meta-data/instance-id')
      publicip = ec2_metadata.get('/latest/meta-data/public-ipv4')
      client.puts("HTTP/1.1 200 OK\r\n\r\n")
      client.puts("<html><body><h1>Graviton University Ruby Demo</h1>")
      client.puts("<p>Instance Type : " + instancetype + "</p>")
      client.puts("<p>Instance ID : " + instanceid + "</p>")
      client.puts("<p>Server public ip : " + publicip + "</p>")
      client.puts("<p>Runtime is : " + `ruby -v` + "</p>")
      client.puts("<p>OS Kernel Version is : " + `uname -r` + "</p>")
      #client.puts("<p>Request from : "+ clientaddr +"</p>")
      client.puts("</body></html>")
  end

  client.close
end
}
server.close  

rescue Interrupt => e

  puts(e)
rescue Exception => e
  puts(e)
  
end