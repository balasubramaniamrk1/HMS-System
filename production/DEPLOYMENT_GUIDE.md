# Deployment Guide for HMS on Ubuntu 22.04/24.04

This guide assumes you have a fresh Ubuntu server with only Python installed.

## Prerequisites
- Root access or sudo privileges on the Ubuntu server.
- The HMS project code on your local machine.

## Step 1: Update and Install System Dependencies

Run the following commands on your Ubuntu server:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

## Step 2: Database Setup (PostgreSQL)

1. Log in to the interactive Postgres session:
   ```bash
   sudo -u postgres psql
   ```

2. Create the database and user (replace `hms123$` with a strong password):
   ```sql
   CREATE DATABASE hms_db;
   CREATE USER hms_user WITH PASSWORD 'hms123$';
   ALTER ROLE hms_user SET client_encoding TO 'utf8';
   ALTER ROLE hms_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE hms_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE hms_db TO hms_user;
   ALTER DATABASE hms_db OWNER TO hms_user; -- Important for Django
   \q
   ```

## Step 3: Project Setup

1. **Move Code to Server**:
   You can copy the files from your local machine to the server using `scp` (run this from your local machine):
   ```bash
   # Replace user@your_server_ip with your actual server credentials
   # Assumes you are in the parent directory of HMS
   scp -r HMS ubuntu@your_server_ip:/home/ubuntu/hms_project
   ```
   *Alternatively, if you use Git, clone the repository.*

2. **Navigate to the directory**:
   ```bash
   cd /home/bala/hms_project/HMS
   ```

3. **Delete old Mac venv (if exists) and Create New**:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python Dependencies**:
   ```bash
   pip install -r production/requirements.txt
   ```

5. **Configure Environment Variables**:
   Create a `.env` file based on the example:
   ```bash
   cp production/env.example .env
   nano .env
   ```
   *Update the `DB_PASSWORD` and `SECRET_KEY` in the `.env` file.*
   *Set ALLOWED_HOSTS=localhost,127.0.0.1,YOUR_SERVER_IP*

6. **Prepare the Application**:
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Apply database migrations
   python manage.py migrate
   
   # Create a superuser
   python manage.py createsuperuser
   ```

## Step 4: Configure Gunicorn (Application Server)

1. **Test Gunicorn Manually** (Optional):
   ```bash
   gunicorn --bind 0.0.0.0:8000 hms_project.wsgi
   ```
   *Visit `http://your_server_ip:8000` to verify it loads. Press Ctrl+C to stop.*

2. **Setup Systemd Service**:
   Copy the service file provided in the production folder to the systemd directory.
   
   *Check the file `production/gunicorn.service` first to ensure the paths match your installation (`/home/bala/hms_project/HMS`).*

   ```bash
   sudo cp production/gunicorn.service /etc/systemd/system/
   ```

3. **Start and Enable Gunicorn**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start gunicorn
   sudo systemctl enable gunicorn
   sudo systemctl status gunicorn
   ```

## Step 5: Configure Nginx (Web Server)

1. **Setup Nginx Configuration**:
   Copy the nginx config file to the sites-available directory.

   *Edit `production/nginx.conf` first to replace `YOUR_DOMAIN_OR_IP` with your actual IP address or domain name.*
   *Ensure paths point to `/home/bala/hms_project/HMS/staticfiles` and `/home/bala/hms_project/HMS/media`.*
   *Ensure proxy_pass points to `http://unix:/run/gunicorn/gunicorn.sock`.*

   ```bash
   sudo cp production/nginx.conf /etc/nginx/sites-available/hms_project
   ```

2. **Enable the Configuration**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/hms_project /etc/nginx/sites-enabled/
   ```

3. **Remove Default Nginx Config**:
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

4. **Test and Restart Nginx**:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Firewall Setup**:
   ```bash
   sudo ufw allow 'Nginx Full'
   ```

## Step 6: Troubleshooting

- **Check Logs**:
  - Gunicorn: `sudo journalctl -u gunicorn`
  - Nginx: `sudo tail -f /var/log/nginx/error.log`

- **Static Files 404**:
  Ensure `STATIC_ROOT` in `settings.py` matches the Nginx config (`/home/bala/hms_project/HMS/staticfiles`).
