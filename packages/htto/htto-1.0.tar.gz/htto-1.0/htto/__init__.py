from json import loads
from re import search
from ssl import create_default_context, SSLSocket
from socket import socket, AF_INET, SOCK_STREAM
from typing import Optional, Union
from urllib.parse import urlencode, urlparse
# from certifi import where

def extract_port(url:str) -> int:
    if len(url.split(':')) == 3 or ':' in url and ':/' not in url:
        return url.split(':')[2]
    elif 'http://' in url:
        return 80
    
    return 443

def new_connection(host:str, port:int, time_out:int) -> socket | SSLSocket:
    connection = socket(AF_INET, SOCK_STREAM)
    connection.connect((host, port))

    if port == 80:
        connection.setblocking(False)
        connection.settimeout(time_out)
        return connection
    else:
        context = create_default_context()
        # context.load_verify_locations(where())
        ssl_connection = context.wrap_socket(connection, server_hostname=host)
        ssl_connection.setblocking(0)
        ssl_connection.settimeout(time_out)
        return ssl_connection

def new_raw_request(method, api, headers, data) -> str:
    return f"""{method} {api} HTTP/1.1\r
{headers}
\r
{data}
"""

class client:
    def __init__(self, timeout:int=10) -> None:
        self.time_out : int = timeout
        self.running : bool = False
        self.hosts : dict = {}

    def close_host(self, host) -> str:
        try:
            self.hosts[host].close()
            return f"'{host}' is closed"
        except:
            f"'{host}' not found"
    
    def close(self) -> str:
        for host in self.hosts.values():
            host.close()
        return 'closed'

    def action(self, request:str, host:str) -> str:
        self.running = True
        self.hosts[host].sendall(request.encode('utf-8'))
        body : str = ''
        loop : bool = False

        while True:
            try:
                response = self.hosts[host].recv(4096)
                body += response.decode('utf-8')
                loop = True
            except:
                if loop:
                    break
        
        self.running = False
        return body

    def delete(self, url:str, headers:dict={}):
        return self.get(url, headers, 'DELETE')
    
    def put(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PUT')
    
    def patch(self, url:str, headers:dict={}, data=Optional[Union[str, dict]]):
        return self.post(url, headers, data, 'PATCH')

    def post(self, url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
        host : str = urlparse(url).hostname

        if type(data) == dict:
            data = urlencode(data)
        else:
            data = data

        if host not in self.hosts:
            self.hosts[host] = new_connection(host, extract_port(url), time_out=self.time_out)

        my_headers = f'Host: {host}\r\nConnection: keep-alive\r\n'
        if 'user-agent' not in headers and 'User-Agent' not in headers:
            my_headers += 'User-Agent: Mozilla/5.0 Firefox/132.0\r\n'

        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'
        my_headers += 'Content-Length: ' + str(len(data)) + '\r'

        if self.running:
            return 'this client under used, create new client in same host'

        return ExtractResponses(self.action(new_raw_request(method, url.split(host)[1:][0] or '/', my_headers, data), host))

    def get(self, url:str, headers:dict={}, method:str='GET'):
        host : str = urlparse(url).hostname

        if host not in self.hosts:
            self.hosts[host] = new_connection(host, extract_port(url), time_out=self.time_out)

        my_headers = f'Host: {host}\r\nConnection: keep-alive\r\n'
        if 'user-agent' not in headers and 'User-Agent' not in headers:
            my_headers += 'User-Agent: Mozilla/5.0 Firefox/132.0\r\n'
        
        for key, value in headers.items():
            my_headers += key + ': ' + value + '\r\n'

        if self.running:
            return 'this client under used, create new client in same host'
        
        return ExtractResponses(self.action(new_raw_request(method, url.split(host)[1:][0] or '/', my_headers, ''), host))

class ExtractResponses:
    def __init__(self, response):
        self.response:str = response

    def __str__(self) -> str:
        return f"status_code: {search(r'HTTP/1.1 (\d{3} .*)', self.response).group(1)}"

    def status_code(self):
        self.__str__()

    def json(self) -> dict:
        return loads(self.body())

    def text(self) -> str:
        return self.body()

    def body(self) -> str:
        return str(self.response.split('\r\n\r\n')[1])
    
    def headers(self) -> dict:
        for_return : dict = {}
        for_nothing : list = self.response.splitlines()[1:]

        for res in for_nothing:
            if not res.__contains__(': '):
                break
            for_split = res.split(': ')
            for_return[for_split[0]] = res.removeprefix(for_split[0] + ': ')

        return for_return

def get(url:str, headers:dict={}, method:str='GET'):
    cn = client(timeout=10)
    for_return = cn.get(url, headers, method)
    cn.close()
    return for_return

def post(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='POST'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return

def delete(url:str, headers:dict={}, method:str='DELETE'):
    cn = client(timeout=10)
    for_return = cn.get(url, headers, method)
    cn.close()
    return for_return

def patch(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PATCH'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return

def put(url:str, headers:dict={}, data=Optional[Union[str, dict]], method:str='PUT'):
    cn = client(timeout=10)
    for_return = cn.post(url, headers, data, method)
    cn.close()
    return for_return