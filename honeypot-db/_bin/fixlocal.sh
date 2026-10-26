#!/bin/bash
sudo service apache2 stop 2>/dev/null
sudo touch /var/log/honeypot.log
sudo chmod 666 /var/log/honeypot.log
sudo nohup python3 /opt/honeypot/honeypot.py >/dev/null 2>&1 &
