# ADSLProxy
基于ADSL拨号的VPS的代理IP服务

# 原理
1. 准备一个能ADSL拨号的VPS(Client)，并在上面搭建一个squid代理服务。
2. 准备一个有固定IP的Server，并在上面搭建一个简单的web服务。
3. 在Client上定时拨号产生新的IP，并将新的IP传送到Server
4. 使用者请求Server获取最新的动态IP

# 使用

## Client && Server
```bash
git clone https://github.com/nghuyong/ADSLProxy.git
cd ADSLProxy
pip install -r requirements.txt
```
## Client
需要用root用户执行，因为ADSL拨号的权限级别较高
```bash
vim /etc/crontab
```
输入：(每隔10分钟更换一次IP)
```bash
0,10,20,30,43,50 * * * * root cd /path/to/ADSLProxy && python client.py
```
保存退出，并重启crond

```bash
service crond restart
```
## Server
启动web服务
```bash
nohup python server.py &
```

## API使用
```bash
Get http://IP:8080/api/proxy?auth=my_auth
```
```json
{
    "data": {
        "00155d0e02d7": {
            "time": "2018-11-15 20:50:07",
            "port": 8877,
            "ip": "125.121.112.244"
        }
    },
    "code": 0,
    "count": 1
}
```

# Note

## Centos上squid的配置
```bash
#
# Recommended minimum configuration:
#
acl manager proto cache_object
acl localhost src 127.0.0.1/32 ::1
acl to_localhost dst 127.0.0.0/8 0.0.0.0/32 ::1

# Example rule allowing access from your local networks.
# Adapt to list your (internal) IP networks from where browsing
# should be allowed
acl localnet src 10.0.0.0/8	# RFC1918 possible internal network
acl localnet src 172.16.0.0/12	# RFC1918 possible internal network
acl localnet src 192.168.0.0/16	# RFC1918 possible internal network
acl localnet src fc00::/7       # RFC 4193 local private network range
acl localnet src fe80::/10      # RFC 4291 link-local (directly plugged) machines

acl SSL_ports port 443
acl Safe_ports port 80		# http
acl Safe_ports port 21		# ftp
acl Safe_ports port 443		# https
acl Safe_ports port 70		# gopher
acl Safe_ports port 210		# wais
acl Safe_ports port 1025-65535	# unregistered ports
acl Safe_ports port 280		# http-mgmt
acl Safe_ports port 488		# gss-http
acl Safe_ports port 591		# filemaker
acl Safe_ports port 777		# multiling http
acl CONNECT method CONNECT

#
# Recommended minimum Access Permission configuration:
#
# Only allow cachemgr access from localhost
http_access allow manager localhost
http_access deny manager

# Deny requests to certain unsafe ports
http_access deny !Safe_ports

# Deny CONNECT to other than secure SSL ports
http_access deny CONNECT !SSL_ports

# We strongly recommend the following be uncommented to protect innocent
# web applications running on the proxy server who think the only
# one who can access services on "localhost" is a local user
#http_access deny to_localhost

#
# INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS
#

# Example rule allowing access from your local networks.
# Adapt localnet in the ACL section to list your (internal) IP networks
# from where browsing should be allowed
http_access allow localnet
http_access allow localhost

# And finally deny all other access to this proxy
auth_param basic program /usr/lib64/squid/ncsa_auth /etc/squid/passwd
acl auth_user proxy_auth REQUIRED
http_access allow auth_user
#http_access allow all

# Squid normally listens to port 3128
http_port 8877

# Uncomment and adjust the following to add a disk cache directory.
#cache_dir ufs /var/spool/squid 100 16 256

# Leave coredumps in the first cache dir
coredump_dir /var/spool/squid

# Add any of your own refresh_pattern entries above these.
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern .               0       20%     4320

# 配置高匿，不允许设置任何多余头信息，保持原请求header。
request_header_access Via deny all
request_header_access X-Forwarded-For deny all
```

## Centos 关闭防火墙
`poweroff`

# Reference
[Python爬虫进阶七之设置ADSL拨号服务器代理| 静觅](https://cuiqingcai.com/3443.html)