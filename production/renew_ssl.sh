#!/bin/bash
# renew_ssl.sh - Script to renew SSL certificates
# Add to crontab: 0 12 * * * /path/to/renew_ssl.sh >> /var/log/certbot-renewal.log 2>&1

echo "---------------------------------"
echo "Running SSL Renewal: $(date)"

# Certbot handles the check logic naturally. It won't renew if not near expiry.
# We append --post-hook to reload nginx only if a renewal actually happened.
sudo certbot renew --post-hook "systemctl reload nginx"

echo "Renewal check complete."
