from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import group_required

@login_required
def doctor_console(request):
    """
    Dashboard for Doctors to view appointments and patients.
    """
    # Placeholder context
    context = {
        'appointments': [], # Fetch actual appointments later
        'patients': []
    }
    return render(request, 'doctors/console/dashboard.html', context)
