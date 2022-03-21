#!/bin/bash
#Alpine Linux:
apk update
apk add bash
apk add --no-cache vim
apk add --no-cache py3-virtualenv 
apk add --no-cache python3 py3-pip
pip install virtualenv
python3 -m pip install --user virtualenv
python3 -m venv venv
pip install pgadmin4
python3 /pgadmin4/setup.py --load-servers data/server/nucamp_server.json
#virtualenv pgadmin4

# # Debian Linux
# apt-get update
# apt update
# apt-get -y install curl
# apt-get -y install sudo
# user od -AG edwardp
# more /etc/sudoers
# curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add
# #sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
# sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/focal/ pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
# apt-get -y install vim
# apt-get -y install python3-pip
# #apt-get -y install python-virtualenv
# pip install virtualenv
# # pip install Flask
# # pip install Flask-SocketIO
# # pip install Flask-Babel
# pip install pgadmin4
# # apt install -y pgadmin4
# python3 /usr/pgadmin4/web/setup.py --load-servers data/server/nucamp_server.json