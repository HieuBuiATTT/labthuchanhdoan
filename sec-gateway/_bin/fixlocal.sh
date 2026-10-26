#!/bin/bash
sudo mkdir -p /var/log/suricata
sudo touch /var/log/suricata/fast.log
sudo chmod 666 /var/log/suricata/fast.log
echo "[**] [1:100001:1] SURICATA SSRF Private IP Probing Detected [**]" >> /var/log/suricata/fast.log
