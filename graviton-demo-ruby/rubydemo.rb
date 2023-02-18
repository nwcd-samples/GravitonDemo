require 'socket'
require 'uri'
require 'net/http'

def getmetadata(url)
  uri = URI(url)
  res = Net::HTTP.get_response(uri)
  return res.body if res.is_a?(Net::HTTPSuccess)
end
server = TCPServer.new '0.0.0.0' ,5000

loop do                                                  

  client = server.accept
  first_line = client.gets
  verb, path, _ = first_line.split

  if verb == 'GET'
    #if result = path.match(/^\/customers\/(.*?)$/)
      #client_id = result[1]
      instancetype = getmetadata('http://169.254.169.254/latest/meta-data/instance-type')
      instanceid = getmetadata('http://169.254.169.254/latest/meta-data/instance-id')
      publicip = getmetadata('http://169.254.169.254/latest/meta-data/public-ipv4')
      
      client.puts("HTTP/1.1 200 OK\r\n\r\n")
      client.puts("<html><body><h1>Graviton University Python Demo</h1>")
      client.puts("<p>Instance Type : " + instancetype + "</p>")
      client.puts("<p>Instance ID : " + instanceid + "</p>")
      client.puts("<p>Server public ip : " + publicip + "</p>")
      client.puts("</body></html>")
    #end
  end

  client.close
end

server.close  
