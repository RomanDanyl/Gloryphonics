#!/bin/bash

DOMAIN="gloryphonic-api.ddns.net"
CERT_PATH="./certbot/conf/live/$DOMAIN/fullchain.pem"
DAYS_LEFT=2   # мінімум днів дії, щоб НЕ оновлювати

# Move to the directory where this script is located
cd "$(dirname "$0")" || {
  echo "❌ Failed to change to script directory"
  exit 1
}

if [ -f "$CERT_PATH" ]; then
  # обчислюємо дату закінчення
  EXPIRY_DATE=$(openssl x509 -enddate -noout -in "$CERT_PATH" | cut -d= -f2)
  EXPIRY_SECONDS=$(date -d "$EXPIRY_DATE" +%s)
  NOW_SECONDS=$(date +%s)
  SECONDS_LEFT=$((EXPIRY_SECONDS - NOW_SECONDS))
  DAYS_REMAINING=$((SECONDS_LEFT / 86400))

  echo "📜 Certificate for $DOMAIN expires in $DAYS_REMAINING days"

  if [ $DAYS_REMAINING -gt $DAYS_LEFT ]; then
    echo "✅ Certificate is still valid for more than $DAYS_LEFT days. Skipping renewal."
    exit 0
  fi
else
  echo "⚠️ No certificate found for $DOMAIN. Will attempt to issue a new one..."
fi

echo "🔄 Renewing SSL certificate..."

# Run Certbot in a temporary container to renew the certificate
docker compose run --rm certbot certonly \
  --webroot --webroot-path=/var/www/certbot \
  --quiet \
  --email gloryphonic@gmail.com \
  --agree-tos \
  -d $DOMAIN

CERTBOT_EXIT_CODE=$?

if [ $CERTBOT_EXIT_CODE -ne 0 ]; then
  echo "❌ Certbot failed with exit code ($CERTBOT_EXIT_CODE)"
  exit $CERTBOT_EXIT_CODE
fi

echo "✅ Certificate renewed successfully. Reloading Nginx..."

docker compose exec nginx nginx -s reload
NGINX_EXIT_CODE=$?

if [ $NGINX_EXIT_CODE -ne 0 ]; then
  echo "❌ Failed to reload Nginx ($NGINX_EXIT_CODE)"
  exit $NGINX_EXIT_CODE
fi

echo "🎉 Renewal and reload completed successfully!"
