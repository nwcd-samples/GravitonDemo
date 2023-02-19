#!/usr/bin/env python3

import socket, sys
import urllib.request
import subprocess

MAX_PACKET = 32768


def getcommands(cmd):
    status, output = subprocess.getstatusoutput(cmd)
    return output


def getmetadata(url):
    response = urllib.request.urlopen(url)
    response_text = response.read().decode('utf8')
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
                _data = sock.recv(MAX_PACKET)
                rdata.append(str(_data, 'utf8'))
            except socket.timeout:
                return ''.join(rdata)

        # unreachable
    finally:
        sock.settimeout(prev_timeout)


def normalize_line_endings(s):
    r'''Convert string containing various line endings like \n, \r or \r\n,
    to uniform \n.'''

    return ''.join((line + '\n') for line in s.splitlines())


def send_resp(client_sock, content, encoding='utf8'):
    client_sock.send(content.encode(encoding))


def run():
    r'''Main loop'''

    # Create TCP socket listening on 5003 port for all connections,
    # with connection queue of length 1
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                                socket.IPPROTO_TCP)
    server_sock.bind(('0.0.0.0', 5003))
    server_sock.listen(1)

    while True:
        client_sock = None
        try:
            # accept connection
            client_sock, client_addr = server_sock.accept()

            request = normalize_line_endings(recv_all(client_sock))  # hack again

            response_body = [
                '<html><body><h1>Graviton University Python Demo</h1>',
                '<p>Instance Type : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/instance-type'),
                '<p>Instance ID : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/instance-id'),
                '<p>Server public ip : %s</p>' % getmetadata('http://169.254.169.254/latest/meta-data/public-ipv4'),
                '<p>Runtime is : %s</p>' % sys.version,
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

            response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in
                                        response_headers.items())

            # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
            response_proto = 'HTTP/1.1'
            response_status = '200'
            response_status_text = 'OK'  # this can be random

            # sending all this stuff
            send_resp(client_sock, '%s %s %s' %
                    (response_proto, response_status, response_status_text))
            send_resp(client_sock, response_headers_raw)
            send_resp(client_sock, '\n')  # to separate headers from body
            send_resp(client_sock, response_body_raw)
        except KeyboardInterrupt:
            if client_sock:
                # closing connection, as we stated before
                client_sock.close()
            break

run()
