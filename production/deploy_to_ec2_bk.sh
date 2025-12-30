#!/bin/bash

# Configuration
SERVER_USER="bala"      # The user to run the application (will be created if missing)
SERVER_IP="$1"          # Pass IP as first argument
DOMAIN_NAME="$2"        # Domain name for SSL
EMAIL="$3"              # Email for Let's Encrypt
SSH_KEY="$4"            # Private Key File (.pem)
SSH_USER="${5:-ubuntu}" # User to connect as (default: ubuntu)

PROJECT_DIR="/home/$SERVER_USER/hms_project"
APP_DIR="$PROJECT_DIR/HMS"
DB_NAME="hms_db"
DB_USER="hms_user"
DB_PASSWORD="hms123$" # In production, use environment variables or a secrets manager
SECRET_KEY="Qhzy6r_UNiJM7uWn4PAC0h7De-hrtzJZk-8iapTdJiAQy-I4T0gkjzCLDis9988IuAU"

if [ -z "$SERVER_IP" ] || [ -z "$DOMAIN_NAME" ] || [ -z "$EMAIL" ] || [ -z "$SSH_KEY" ]; then
    echo "Usage: ./deploy_to_ec2.sh <SERVER_IP> <DOMAIN_NAME> <EMAIL> <SSH_KEY_PATH> [SSH_USER]"
    echo "Example: ./deploy_to_ec2.sh 54.x.x.x hms.example.com admin@ex.com ./my-key.pem ubuntu"
    exit 1
fi

# Enable Logging
LOG_FILE="deploy_$(date +%F_%T).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "========================================================"
echo "Deploying HMS to EC2: $SERVER_IP ($DOMAIN_NAME)"
echo "User: $SSH_USER -> $SERVER_USER"
echo "Key: $SSH_KEY"
echo "Database: PostgreSQL (Docker)"
echo "SSL: Enabled via Certbot"
echo "Log File: $LOG_FILE"
echo "========================================================"

# Fix Key Permissions locally
echo "--> Fixing local key permissions..."
chmod 400 "$SSH_KEY"

# Helper for SSH commands
SSH_CMD="ssh -i $SSH_KEY -o StrictHostKeyChecking=no"

# 0. Bootstrap: User Creation, Docker & Dep Installation
echo "==> [1/5] Bootstrapping Server..."
$SSH_CMD -t $SSH_USER@$SERVER_IP << EOF
    set -e
    
    echo "--> Updating System..."
    sudo apt-get update
    sudo apt-get upgrade -y
    
    echo "--> Installing System Dependencies..."
    # Install Python, Nginx, Certbot
    sudo apt-get install -y python3-pip python3-venv python3-dev nginx curl git acl certbot python3-certbot-nginx
    
    echo "--> Installing Docker..."
    if ! command -v docker &> /dev/null; then
        sudo apt-get install -y docker.io
        sudo systemctl enable --now docker
        # Allow default user to run docker
        sudo usermod -aG docker $SSH_USER
    else
        echo "Docker already installed."
    fi

    echo "--> Configuring App User: $SERVER_USER..."
    if id "$SERVER_USER" &>/dev/null; then
        echo "User $SERVER_USER already exists."
    else
        sudo useradd -m -s /bin/bash $SERVER_USER
        sudo usermod -aG sudo $SERVER_USER
        sudo usermod -aG docker $SERVER_USER
    fi
    
    # Setup Passwordless Sudo (Run ALWAYS to ensure it sticks)
    echo "--> Configuring Passwordless Sudo..."
    echo "$SERVER_USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/$SERVER_USER > /dev/null
    sudo chmod 0440 /etc/sudoers.d/$SERVER_USER

    # Ensure SSH access (Idempotent)
    sudo mkdir -p /home/$SERVER_USER/.ssh
    if [ -f ~/.ssh/authorized_keys ]; then
        sudo cp ~/.ssh/authorized_keys /home/$SERVER_USER/.ssh/
        sudo chown -R $SERVER_USER:$SERVER_USER /home/$SERVER_USER/.ssh
        sudo chmod 700 /home/$SERVER_USER/.ssh
        sudo chmod 600 /home/$SERVER_USER/.ssh/authorized_keys
    fi
EOF

# 1. Copy Files to Server (Sync to /tmp first to avoid perm issues)
echo "==> [2/5] Syncing files..."
$SSH_CMD $SSH_USER@$SERVER_IP "rm -rf /tmp/hms_staging && mkdir -p /tmp/hms_staging"
# Sync CURRENT folder content to /tmp/hms_staging
rsync -avz -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" --exclude 'venv' --exclude '__pycache__' --exclude '*.log' --exclude '.git' --exclude '.DS_Store' ./ $SSH_USER@$SERVER_IP:/tmp/hms_staging/

# Move from /tmp to Target (Atomic-ish replacement)
$SSH_CMD $SSH_USER@$SERVER_IP << EOF
    set -e
    echo "--> Moving files to $PROJECT_DIR..."
    sudo mkdir -p $PROJECT_DIR
    # Copy from staging to target (using rsync locally on server or cp)
    # We use rsync locally to update only changed files
    sudo rsync -a /tmp/hms_staging/ $PROJECT_DIR/
    sudo chown -R $SERVER_USER:$SERVER_USER $PROJECT_DIR
    rm -rf /tmp/hms_staging
EOF

# 2. Remote Setup
echo "==> [3/5] Configuring Remote Application..."
$SSH_CMD -t $SERVER_USER@$SERVER_IP << EOF
    set -e

    # Database Setup (Docker)
    echo "--> Setting up Dockerized PostgreSQL..."
    if [ ! "\$(docker ps -q -f name=hms_db_container)" ]; then
        if [ "\$(docker ps -aq -f name=hms_db_container)" ]; then
            echo "Starting existing DB container..."
            docker start hms_db_container
        else
            echo "Creating new DB container..."
            docker run -d \\
                --name hms_db_container \\
                --restart always \\
                -e POSTGRES_DB=$DB_NAME \\
                -e POSTGRES_USER=$DB_USER \\
                -e POSTGRES_PASSWORD='$DB_PASSWORD' \\
                -v hms_pgdata:/var/lib/postgresql/data \\
                -p 5432:5432 \\
                postgres:15
            
            echo "Waiting for DB to initialize..."
            sleep 10
        fi
    else
        echo "DB Container is running."
    fi

    # Venv Setup
    echo "--> Setting up Python Virtual Environment..."
    if [ ! -d "$APP_DIR/venv" ]; then
        python3 -m venv $APP_DIR/venv
    fi
    
    # Install Requirements
    echo "--> Installing Python Requirements..."
    $APP_DIR/venv/bin/pip install --upgrade pip
    $APP_DIR/venv/bin/pip install -r $PROJECT_DIR/requirements.txt || echo "Warning: requirements.txt not found in expected path, trying $APP_DIR" 

    # Environment Variables
    echo "--> Configuring .env..."
    cat > $APP_DIR/.env << ENV
SECRET_KEY='$SECRET_KEY'
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,$SERVER_IP,$DOMAIN_NAME
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
    sed -i "s|User=ubuntu|User=$SERVER_USER|g" $PROJECT_DIR/gunicorn.service
    sed -i "s|/home/ubuntu/hms_project|$APP_DIR|g" $PROJECT_DIR/gunicorn.service
    sed -i "s|WorkingDirectory=.*|WorkingDirectory=$APP_DIR|g" $PROJECT_DIR/gunicorn.service
    sed -i "s|ExecStart=.*|ExecStart=$APP_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn/gunicorn.sock hms_project.wsgi:application|g" $PROJECT_DIR/gunicorn.service
    
    sudo cp $PROJECT_DIR/gunicorn.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn
    sudo systemctl restart gunicorn

    # Nginx Setup (HTTP First)
    echo "--> Configuring Nginx (Initial HTTP)..."
    sed -i "s|YOUR_DOMAIN_OR_IP|$DOMAIN_NAME|g" $PROJECT_DIR/nginx.conf
    sed -i "s|root /home/ubuntu/hms_project/staticfiles|root $APP_DIR/staticfiles|g" $PROJECT_DIR/nginx.conf
    sed -i "s|root /home/ubuntu/hms_project/media|root $APP_DIR/media|g" $PROJECT_DIR/nginx.conf
    # Fallback cleanup just in case
    sed -i "s|root /home/bala/hms_project/HMS/staticfiles|root $APP_DIR/staticfiles|g" $PROJECT_DIR/nginx.conf 
    
    sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/hms_project
    sudo ln -sf /etc/nginx/sites-available/hms_project /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ufw allow 'Nginx Full'

    echo "Application deployed on HTTP."
EOF

# 3. SSL Setup
echo "==> [4/5] Setting up SSL..."
$SSH_CMD -t $SERVER_USER@$SERVER_IP << EOF
    set -e
    echo "--> Requesting Let's Encrypt Certificate..."
    # Uses --nginx plugin to automatically modify config and setup redirect
    sudo certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email $EMAIL --redirect
    
    echo "--> Reloading Nginx..."
    sudo systemctl reload nginx
EOF

echo "========================================================"
echo "Deployment Complete!"
echo "URL: https://$DOMAIN_NAME"
echo "Log File: $LOG_FILE"
echo "========================================================"
