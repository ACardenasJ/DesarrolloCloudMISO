#!/bin/bash

sudo apt-get update
sudo apt-get install curl -y
sudo apt-get install gnupg -y
sudo apt-get install ca-certificates -y
sudo apt-get install lsb-release -y
sudo apt-get install docker.io -y
sudo groupadd docker
sudo usermod -aG docker $USER
sudo service docker restart
sudo docker ps
if [ -d "DesarrolloCloudMISO" ]; then
    echo "DesarrolloCloudMISO folder already exists"
else
    git clone https://github.com/ACardenasJ/DesarrolloCloudMISO.git
fi
cd DesarrolloCloudMISO/
git checkout release
git fetch
git pull
cd DesarrolloCloudApiConverter/Backend/
sudo apt install docker-compose -y
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy && chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=misonube2022equipo23:us-central1:csql-misocloud-postgres=tcp:5432 2>&1 &
sudo docker-compose up --build

