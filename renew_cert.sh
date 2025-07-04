#!/bin/bash

docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --quiet --renew-by-default --email gloryphonic@gmail.com --agree-tos -d gloryphonic-api.ddns.net

docker compose exec nginx nginx -s reload