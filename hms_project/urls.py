"""
URL configuration for hms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views # Import core views

# Custom Admin Site Headers
admin.site.site_header = "Admin Console"
admin.site.site_title = "Admin Console"
admin.site.index_title = "Welcome to Admin Console"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    path('blog/', include('blog.urls')),
    path('staff/', include('staff_mgmt.urls')),
    path('inventory/', include('inventory.urls')),
    path('reputation/', include('reputation.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('billing/', include('billing.urls')),
    path('admissions/', include('admissions.urls')),
    
    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', core_views.custom_logout, name='logout'),
    path('admin-access/', core_views.admin_access, name='admin_access'), # New Admin Access Logic
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
