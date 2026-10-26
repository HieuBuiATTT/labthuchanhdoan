#!/bin/bash
sudo service apache2 stop 2>/dev/null
sudo touch /var/log/syslog
sudo chmod 666 /var/log/syslog
sudo nohup python3 /var/www/html/app.py >/dev/null 2>&1 &
