#!/bin/bash

sudo apt-get update
sudo apt-get install -y curl zip
sudo apt install -y gettext-base moreutils
sudo apt-get update
sudo apt-get install cron
sudo chmod +x /home/ubuntu/ec2-caller.sh


crontab<<EOF
*/10 * * * * /home/ubuntu/ec2-caller.sh
EOF



