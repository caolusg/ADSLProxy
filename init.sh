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