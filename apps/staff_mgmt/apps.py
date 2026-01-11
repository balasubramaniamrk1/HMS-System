from django.apps import AppConfig

class StaffMgmtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'staff_mgmt'

    def ready(self):
        import staff_mgmt.signals
