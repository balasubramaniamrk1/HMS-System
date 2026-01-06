import logging
import os

# Ensure logs directory exists
# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Configure Audit Logger
audit_logger = logging.getLogger('hms_audit')
audit_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(LOG_DIR, 'hms_audit.log'))
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)

audit_logger.addHandler(file_handler)

def log_admin_action(user, action, details):
    """
    Helper to log admin actions.
    """
    message = f"User: {user.username} | Action: {action} | Details: {details}"
    audit_logger.info(message)
