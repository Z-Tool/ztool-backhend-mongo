#!/usr/bin/env bash

YELLOW='\033[1;33m'
NC='\033[0m'
SERVER='root@vps.jarrekk.com'

cat << EOF > ./.env
FLASK_CONFIG=$1
SECRET_KEY=$2
IPINFODBKEY=$3
EOF

ALL=$(ssh $SERVER docker ps |grep nginx | wc -l)

if [ $ALL -eq 0 ];then
    echo "${YELLOW}Now deploy all docker container...${NC}"
    fab rebuild && fab up
else
    echo "${YELLOW}Now deploy flask & celery...${NC}"
    fab rebuild:flask && fab up:flask
    fab rebuild:celery && fab up:celery
fi
