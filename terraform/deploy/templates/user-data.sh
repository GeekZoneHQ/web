#!/bin/bash

sudo apt-get update
sudo apt-get install -y curl zip pip3 python
sudo apt install -y gettext-base moreutils
sudo apt-get update
sudo apt-get install cron

sudo pip3 install requests pipenv 

sudo chmod +x /home/ubuntu/ec2-caller.sh


crontab<<EOF
*/3 * * * * /home/ubuntu/ec2-caller.sh
EOF



