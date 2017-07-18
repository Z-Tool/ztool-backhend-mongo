#!/usr/bin/env bash
# author: Kun Jia
# date: 7/18/17
# email: me@jarrekk.com
apt-get update
apt-get install git -y
git clone https://github.com/letsencrypt/letsencrypt
cd letsencrypt
./letsencrypt-auto renew
#./certbot-auto renew
#./letsencrypt-auto certonly --renew-by-default --email me@jack003.com -a manual -d vps.jarrekk.com -d api.jarrekk.com -d vps.jack003.com
