#!/bin/bash

# Move to the directory where this script is located
cd "$(dirname "$0")" || {
  echo "❌ Failed to change to script directory"
  exit 1
}

echo "🔄 Renewing SSL certificate..."

# Run Certbot in a temporary container to renew the certificate
docker compose run --rm certbot certonly \
  --webroot --webroot-path=/var/www/certbot \
  --quiet --renew-by-default \
  --email gloryphonic@gmail.com \
  --agree-tos \
  -d gloryphonic-api.ddns.net

CERTBOT_EXIT_CODE=$?

# Check if Certbot succeeded
if [ $CERTBOT_EXIT_CODE -ne 0 ]; then
  echo "❌ Certbot failed with exit code ($CERTBOT_EXIT_CODE)"
  exit $CERTBOT_EXIT_CODE
fi

echo "✅ Certificate renewed successfully. Reloading Nginx..."

# Reload Nginx inside the container to apply the new certificate
docker compose exec nginx nginx -s reload

NGINX_EXIT_CODE=$?

# Check if Nginx reload succeeded
if [ $NGINX_EXIT_CODE -ne 0 ]; then
  echo "❌ Failed to reload Nginx ($NGINX_EXIT_CODE)"
  exit $NGINX_EXIT_CODE
fi

echo "🎉 Renewal and reload completed successfully!"
