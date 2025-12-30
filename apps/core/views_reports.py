from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def reports_dashboard(request):
    """
    Central hub for reports.
    """
    return render(request, 'core/reports_dashboard.html')
