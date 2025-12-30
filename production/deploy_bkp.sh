#!/bin/bash

# Configuration
SERVER_USER="bala"
SERVER_IP="$1"  # Pass IP as first argument
PROJECT_DIR="/home/$SERVER_USER/hms_project"
APP_DIR="$PROJECT_DIR/HMS"
DB_NAME="hms_db"
DB_USER="hms_user"
DB_PASSWORD="hms123$" # ideally this should be a secret
SECRET_KEY="Qhzy6r_UNiJM7uWn4PAC0h7De-hrtzJZk-8iapTdJiAQy-I4T0gkjzCLDis9988IuAU"

if [ -z "$SERVER_IP" ]; then
    echo "Usage: ./deploy.sh <SERVER_IP>"
    exit 1
fi

echo "Deploying to $SERVER_USER@$SERVER_IP..."

# 1. Copy Files to Server
echo "==> Syncing files..."
# Create parent dir if not exists
ssh $SERVER_USER@$SERVER_IP "mkdir -p $PROJECT_DIR"
# Copy HMS folder (excluding venv via rsync or scp)
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' ../HMS $SERVER_USER@$SERVER_IP:$PROJECT_DIR/

# 2. Remote Setup
echo "==> Configuring Remote Server..."
ssh -t $SERVER_USER@$SERVER_IP << EOF
    set -e

    # Update and Install Deps
    echo "--> Installing System Dependencies..."
    sudo apt update
    sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl

    # Database Setup (Idempotent: only creates if not exists)
    echo "--> Setting up Database..."
    # Check if DB exists, if not create
    if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
        sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
        sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
        sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
        sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
        sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
        sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;" 
        echo "Database created."
    else
        echo "Database already exists."
    fi

    # Venv Setup
    echo "--> Setting up Python Virtual Environment..."
    if [ ! -d "$APP_DIR/venv" ]; then
        python3 -m venv $APP_DIR/venv
    fi
    
    # Install Requirements
    echo "--> Installing Python Requirements..."
    $APP_DIR/venv/bin/pip install -r $APP_DIR/production/requirements.txt

    # Environment Variables
    echo "--> Configuring .env..."
    cat > $APP_DIR/.env << ENV
SECRET_KEY='$SECRET_KEY'
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,$SERVER_IP
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432
ENV

    # Django Management Commands
    echo "--> Running Django Commands..."
    $APP_DIR/venv/bin/python $APP_DIR/manage.py collectstatic --noinput
    $APP_DIR/venv/bin/python $APP_DIR/manage.py migrate

    # Gunicorn Setup
    echo "--> Configuring Gunicorn..."
    # We need to ensure the service file has the correct paths/user. 
    # We will overwrite the user/paths in the uploaded service file dynamically using sed
    sed -i "s|User=ubuntu|User=$SERVER_USER|g" $APP_DIR/production/gunicorn.service
    sed -i "s|/home/ubuntu/hms_project|$APP_DIR|g" $APP_DIR/production/gunicorn.service
    # Also fix the specific path if it was generic in source
    sed -i "s|WorkingDirectory=.*|WorkingDirectory=$APP_DIR|g" $APP_DIR/production/gunicorn.service
    sed -i "s|ExecStart=.*|ExecStart=$APP_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn/gunicorn.sock hms_project.wsgi:application|g" $APP_DIR/production/gunicorn.service
    
    sudo cp $APP_DIR/production/gunicorn.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn
    sudo systemctl restart gunicorn

    # Nginx Setup
    echo "--> Configuring Nginx..."
    sed -i "s|YOUR_DOMAIN_OR_IP|$SERVER_IP|g" $APP_DIR/production/nginx.conf
    # Update paths in nginx.conf
    sed -i "s|root /home/ubuntu/hms_project/staticfiles|root $APP_DIR/staticfiles|g" $APP_DIR/production/nginx.conf
    sed -i "s|root /home/ubuntu/hms_project/media|root $APP_DIR/media|g" $APP_DIR/production/nginx.conf
    sed -i "s|root /home/bala/hms_project/HMS/staticfiles|root $APP_DIR/staticfiles|g" $APP_DIR/production/nginx.conf # Case where it was already bala
    
    # Ensure Alias for Static (Fixing the double path issue)
    # We replace the entire location block logic if needed, or assume the source file is corrected.
    # For safety, let's just make sure the file we uploaded is correct.
    
    sudo cp $APP_DIR/production/nginx.conf /etc/nginx/sites-available/hms_project
    sudo ln -sf /etc/nginx/sites-available/hms_project /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ufw allow 'Nginx Full'

    echo "==> Deployment Complete! Access at http://$SERVER_IP"
EOF
