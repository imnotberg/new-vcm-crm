from django.contrib import admin
from django.urls import include,path,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/',include('contact_management.urls')),
    re_path(r'anymail/',include('anymail.urls')),
]
