#!/bin/bash
# setup_ssl.sh - Automates SSL setup using Certbot (Let's Encrypt)
# Usage: ./setup_ssl.sh <DOMAIN> [EMAIL]

if [ -z "$1" ]; then
    echo "Usage: $0 <DOMAIN> [EMAIL]"
    echo "Example: $0 hms.example.com admin@example.com"
    exit 1
fi

DOMAIN=$1
EMAIL=$2
NGINX_CONF="/etc/nginx/sites-available/hms_project"

echo "==> Setting up SSL for $DOMAIN..."

# 1. Install Certbot
echo "--> Installing Certbot and Nginx plugin..."
if ! command -v certbot &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y certbot python3-certbot-nginx
else
    echo "Certbot already installed."
fi

# 2. Obtain Certificate
# We use --nginx plugin which automatically edits the config, BUT
# we want to control the config manually for better security/customization OR
# rely on certbot's automation.
# For this script, we'll let certbot modify the config effectively, then we can
# tune it or rely on our pre-configured ssl block in nginx (if we had one).
#
# However, our current nginx.conf is basic HTTP.
# Certbot is smart enough to upgrade HTTP block to HTTPS.

echo "--> Requesting Certificate..."
# Non-interactive mode
if [ -z "$EMAIL" ]; then
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect
else
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email $EMAIL --redirect
fi

# 3. Verify Auto-Renewal
echo "--> Verifying Auto-Renewal..."
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

echo "==> SSL Setup Complete!"
echo "    Access your site at https://$DOMAIN"
