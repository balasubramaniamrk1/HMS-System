# Production Deployment Troubleshooting Log

This document records the issues encountered during the deployment of the HMS project to the Ubuntu server and their solutions.

## 1. Virtual Environment Mismatch
**Issue:**  `python: command not found` or `Exec format error`.
**Cause:** The `venv` folder was copied from macOS. Virtual environments are OS-specific and cannot be transferred between Mac and Linux.
**Solution:**
1.  Deleted the old venv: `rm -rf venv`
2.  Created a new one on Ubuntu: `python3 -m venv venv`
3.  Installed requirements: `pip install -r production/requirements.txt`

## 2. Django Import Error
**Issue:** `ImportError: Couldn't import Django`.
**Cause:** Dependencies were not installed in the new environment, or the wrong `pip` was used (User was `root` but pointing to system python).
**Solution:**
Used the full path to the virtual environment binaries to ensure consistency:
```bash
/home/bala/hms_project/HMS/venv/bin/pip install ...
/home/bala/hms_project/HMS/venv/bin/python manage.py ...
```

## 3. 400 Bad Request
**Issue:** Browser showed "Bad Request (400)" when accessing the IP.
**Cause:** The server's IP address was not in `ALLOWED_HOSTS`.
**Solution:**
Updated `.env` file to include the server IP:
```bash
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.64.4
```

## 4. Gunicorn Service User Error (217/USER)
**Issue:** Service failed with status `217/USER`.
**Cause:** The service file was configured for user `ubuntu`, but the actual user was `bala`.
**Solution:**
Edited `/etc/systemd/system/gunicorn.service` to set:
```ini
User=bala
WorkingDirectory=/home/bala/hms_project/HMS
ExecStart=/home/bala/hms_project/HMS/venv/bin/gunicorn ...
```

## 5. Gunicorn Socket Permission Error
**Issue:** Gunicorn failed to create the socket file in `/run/`.
**Cause:** Regular users cannot write directly to `/run`.
**Solution:**
1.  Updated `gunicorn.service` to use `RuntimeDirectory`:
    ```ini
    RuntimeDirectory=gunicorn
    ExecStart=... --bind unix:/run/gunicorn/gunicorn.sock ...
    ```
    *(This automatically creates `/run/gunicorn/` with correct permissions)*
2.  Updated Nginx config to match the new socket path:
    ```nginx
    proxy_pass http://unix:/run/gunicorn/gunicorn.sock;
    ```

## 6. Static Files Not Loading (404/403)
**Issue:** Site loaded, but without styles (CSS). Nginx logs showed "No such file" for `.../staticfiles/static/css/...`.
**Cause:** The Nginx `root` directive appends the location path (`/static/`) to the root path, causing a double-nested path looking for `static/static`.
**Solution:**
Changed `root` to `alias` in `/etc/nginx/sites-available/hms_project`.
**Incorrect:**
```nginx
location /static/ { root /path/to/staticfiles; }
```
**Correct:**
```nginx
location /static/ { alias /home/bala/hms_project/HMS/staticfiles/; }
```

## 7. Login Failure (Invalid Credentials)
**Issue:** Unable to log in with existing credentials after deployment.
**Cause:** The production database (PostgreSQL) is fresh and empty; users from the local development database (SQLite) are not transferred automatically.
**Solution:**
Created a new superuser (admin) account on the production server:
```bash
/home/bala/hms_project/HMS/venv/bin/python manage.py createsuperuser
```
Follow the prompts to set a username and password, then try logging in with those exact credentials.

Option 2: Change Password (If you already created a user) If you are sure you created a user but forgot the password, you can reset it:
```bash
/home/bala/hms_project/HMS/venv/bin/python manage.py changepassword <your_username>
```

## 8. Automation (Future Deployments)
**Goal:** Automate the manual steps (file transfer, setup, config updates) for new servers or updates.
**Solution:**
Created `production/deploy.sh` script.
**Usage:**
```bash
./production/deploy.sh <SERVER_IP>
```
**Features:**
- **File Transfer**: Uses `rsync` to copy code (excluding local venv).
- **Setup**: Installs apt/pip packages and sets up the Postgres DB if missing.
- **Config**: Dynamically updates `gunicorn.service` and `nginx.conf` with the correct remote User, IP, and Paths.
- **Fixes**: Automatically applies the static file alias and socket permission fixes.
Prepared proper production configuration (Gunicorn, Nginx, Systemd).
Troubleshetted and fixed critical deployment issues (permissions, static files, database users).
Documented everything in 
TROUBLESHOOTING_LOG.md
.
Automated the future process with 
deploy.sh
.
