# HTTO is high performance and simple HTTP library.

install htto library on windows/linux<br/>
```bash
pip install htto
```
how to use:<br/>
```python3
# 1 import htto library
import htto

# 2 creat client to save your connections session
cn = htto.client(timeout=10)
cn_without_timeout = cn()

# 3 send http request
response = cn.get('https://httpbin.org/ip')

# 4 take response with any format
print(response.json()['origin'])
print(response.text())
print(response.body())
print(response.headers().get('User-Agent'))

# 5 close connection after finish
cn.close_host('httpbin.org')

# 6 close all connections in the client
cn.close()
```

send http request directly<br/>

```python3
import htto

# send http request without client
response = htto.get('https://httpbin.org')
print(response.text())
```

**soon htto will support proxies HTTP, HTTPS, SOCKS4, SOCKS5**<br/>