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
```bash
crontab -e
```
输入：(每隔10分钟更换一次IP)
```bash
0,10,20,30,43,50 * * * * cd /path/to/ADSLProxy && python client.py
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