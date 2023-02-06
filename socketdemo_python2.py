#!/usr/bin/env python

import socket
import urllib2
import commands

MAX_PACKET = 32768

def getcommands(cmd):
    status,output = commands.getstatusoutput(cmd)
    return output

def getmetadata(url):
    response = urllib2.urlopen(url)
    response_text = response.read()
    return response_text

def recv_all(sock):
    r'''Receive everything from `sock`, until timeout occurs, meaning sender
    is exhausted, return result as string.'''

    prev_timeout = sock.gettimeout()
    try:
        sock.settimeout(0.01)

        rdata = []
        while True:
            try:
                rdata.append(sock.recv(MAX_PACKET))
            except socket.timeout:
                return ''.join(rdata)

        # unreachable
    finally:
        sock.settimeout(prev_timeout)

def normalize_line_endings(s):
    r'''Convert string containing various line endings like \n, \r or \r\n,
    to uniform \n.'''

    return ''.join((line + '\n') for line in s.splitlines())

def run():
    r'''Main loop'''

    # Create TCP socket listening on 5000 port for all connections, 
    # with connection queue of length 1
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, \
                                socket.IPPROTO_TCP)
    server_sock.bind(('0.0.0.0', 5000))
    server_sock.listen(1)

    while True:
        # accept connection
        client_sock, client_addr = server_sock.accept()

        request = normalize_line_endings(recv_all(client_sock)) # hack again

        response_body = [
            '<html><body><h1>Graviton University Demo</h1>',
            '<p>Instance Type : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/instance-type'),
            '<p>Instance ID : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/instance-id'),
            '<p>Server public ip : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/public-ipv4'),
            '<p>Runtime is : %s</p>' % getcommands('python --version'),
            '<p>OS Kernel Version is : %s</p>' % getcommands('uname -r'),
            '<p>Request from : %s</p>' % str(client_addr[0]),
            '<ul>',
        ]

        response_body.append('</ul></body></html>')

        response_body_raw = ''.join(response_body)

        # Clearly state that connection will be closed after this response,
        # and specify length of response body
        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(response_body_raw),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                                response_headers.iteritems())

        # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK' # this can be random

        # sending all this stuff
        client_sock.send('%s %s %s' % (response_proto, response_status, response_status_text))
        client_sock.send(response_headers_raw)
        client_sock.send('\n') # to separate headers from body
        client_sock.send(response_body_raw)

        # and closing connection, as we stated before
        client_sock.close()

run()
