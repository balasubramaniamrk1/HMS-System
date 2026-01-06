# 🚀 CI/CD Setup Guide for HMS

I have set up a GitHub Actions workflow that will automatically deploy your changes to the EC2 server whenever you push to the `main` branch.

## 1. The Workflow File
I created the file `.github/workflows/deploy.yml`. This workflow:
1.  Checks out your code.
2.  Sets up the SSH connection using a private key you provide.
3.  Runs your existing `production/deploy_to_ec2.sh` script to sync changes (using `rsync`, which only moves changed files) and restart the server.

## 2. Required GitHub Secrets
For this to work "without hassle", you need to add the following 5 secrets to your GitHub Repository.

### How to Add a Secret
1.  Go to your GitHub Repository page.
2.  Click **Settings** (top tab).
3.  In the left sidebar, click **Secrets and variables** -> **Actions**.
4.  Click the green **New repository secret** button.
5.  Type the **Name** and **Secret** (value) from the table below, then click **Add secret**.

| Secret Name | Value to Enter |
| :--- | :--- |
| `EC2_HOST_IP` | Your EC2 Public IP Address (e.g., `54.x.x.x`). |
| `EC2_SSH_KEY` | Run this command in your terminal: `cat production/hms.pem`.<br>Copy the **entire output** (including `-----BEGIN...` and `-----END...`) and paste it here. |
| `DOMAIN_NAME` | Your domain name (e.g., `hms.yoursite.com`). |
| `EMAIL` | Your email address (e.g., `admin@example.com`). |
| `SSH_USER` | `ubuntu` (This is the default for AWS EC2). |

## 3. How to Deploy

### Automatic Deployment (CI/CD)
1.  Push your code to GitHub:
    ```bash
    git add .
    git commit -m "Enhance HMS features"
    git push origin main
    ```
2.  Go to the **Actions** tab in your GitHub repository to watch the deployment progress.
3.  Once the checkmark turns green, your changes are live on the server!

## 4. Daily Workflow (How to Deploy Future Changes)
**Important:** Your local changes are **NOT** committed automatically. You must manually "save and push" them to trigger the deployment.

Whenever you finish editing code and want to deploy, run these 3 commands in your terminal:

```bash
# 1. Add all changed files to the staging area
git add .

# 2. Commit the changes with a message describing what you did
git commit -m "Describe your change here"

# 3. Push to GitHub (This triggers the auto-deployment)
git push origin main
```
*Wait ~1-2 minutes for GitHub Actions to finish, then check your site.*
