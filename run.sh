#!/bin/sh
echo "Welcome to the Geek.Zone/Web setup script!"
echo "We know you don't have a choice when selecting setup scripts, so we are grateful that you chose this one"
echo "Let's get readyyyyyy to Djangoooooo!\n\n"


# check if setup has been completed in the past

FILE=.setup_done
if test -f "$FILE"; then
    echo "setup has previously completed"
else
  echo "setup has not previously completed"

  # check sudo
  GREEN='\033[0;32m'
  NC='\033[0m'
  if [ $(id -u) != "0" ]; then
     echo "I am not root"
     echo "https://www.youtube.com/watch?v=yJxCdh1Ps48"
     echo "You need this command"
     echo "\n${GREEN}sudo sh setup.sh${NC}\n"
     exit 1
  fi

  echo "I am root."

  # update & upgrade
  apt update -y
  apt upgrade -y

  # Install Python3 & pip
  apt install -y build-essential libssl-dev libffi-dev python3-dev python3-venv python3-pip

  # check python installed successfully
  if [ $(python3 -c 'print("Success")') = "Success" ]
  then
    echo "Python3 installed successfully"
  else
    echo "Python3 install failed, please hang up and try again"
    exit 1
  fi

  exit 0


  # Install nodejs
  apt install nodejs -y

  # install npm
  apt install npm -y

  # Install tailwind
  python3 manage.py tailwind install

  # Create venv
  python3 -m venv env

  # Activate venv
  . env/bin/activate

  # Install requirements
  pip3 install -r requirements.txt

  # create setup completion flag file
  echo "" >> .setup_done
fi

# Migrate db
python3 manage.py makemigrations
python3 manage.py migrate

# run servers, tailwind, livereload, django
gnome-terminal --tab -e python3 manage.py runserver --tab -e python3 manage.py tailwind start --tab -e python3 manage.py livereload

# open the site in the default browser
xdg-open http://localhost:8000/memberships/register </dev/null >/dev/null 2>&1 & disown

# Done!
echo ""
echo "\nTh-a-th-th-a-th-th-a-th-that's all, folks!"
echo "https://www.youtube.com/watch?v=gBzJGckMYO4\n"
exit 0