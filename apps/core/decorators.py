from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def group_required(group_names):
    """
    Decorator to check if user belongs to one of the given groups.
    redirects to Referer or Home with an error message if failed.
    group_names can be a string or a list of strings.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
                
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            if isinstance(group_names, str):
                groups = [group_names]
            else:
                groups = group_names
                
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            
            # Access Denied Logic
            messages.error(request, "You do not have access to this module.")
            referer = request.META.get('HTTP_REFERER')
            
            # Prevent infinite redirect loop if referer is same as current path
            if referer and request.path not in referer:
                return redirect(referer)
            
            # Fallback based on user role roughly, or just home
            if request.user.groups.filter(name='Staff').exists():
                return redirect('staff_attendance') # Staff Dashboard
            elif request.user.groups.filter(name='Doctors').exists():
                return redirect('doctor_console')
            elif request.user.groups.filter(name='Inventory Managers').exists():
                return redirect('inventory_dashboard')
            else:
                return redirect('/') # Home
                
        return _wrapped_view
    return decorator
