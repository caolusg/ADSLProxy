#!/usr/bin/env bash
yum -y install python-pip
yum install -y squid
yum install -y httpd
yum install -y lsof
pip install -r requirements.txt
htpasswd -c /etc/squid/passwd name password
rm /etc/squid/squid.conf
cp squid.conf /etc/squid/squid.conf
systemctl stop firewalld.service
squid stop
squid start
echo "0,5,10,15,20,25,30,35,40,45,50,55 * * * * root cd /root/ADSLProxy && python client.py"  > /etc/crontab
service crond restart