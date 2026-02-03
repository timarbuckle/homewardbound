#!/bin/bash
# run job to update latest cats
cd "$(dirname -- "$(readlink -f "${BASH_SOURCE[0]}")")"
PATH=/home/tim/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
export DISPLAY=:0
echo "stopping cats service ..."
#sudo systemctl stop cats
sudo service cats stop
sleep 2
#sudo systemctl stop cats
echo "updating cats ..."
uv run hbcats/manage.py update
echo "starting cats service ..."
#sudo systemctl start cats
sudo service cats start
