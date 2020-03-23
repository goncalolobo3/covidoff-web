"""covidoff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.views.generic import RedirectView

if settings.COVIDOFF_AUTHENTICATION_DEPLOY:
    
    urlpatterns = [
        path('auth/', include('authnoop.urls')),
    ]

else:

    urlpatterns = [
        
        path('account/', include('access.urls')),
        path('admin/', admin.site.urls),
        path('tracker/', include('tracker.urls'))
    ]

    # Pedir chave pública

    # Healtcare-speciifc URLs
    if settings.COVIDOFF_HEALTHCARE_DEPLOY:
        
        urlpatterns += [
            path('', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL, permanent=False)),
        ]

    # Government-speciifc URLs
    if settings.COVIDOFF_GOVERNMENT_DEPLOY:
        
        urlpatterns += [
            path('', RedirectView.as_view(url=settings.LOGIN_REDIRECT_URL, permanent=False)),
            path('broadcast/', include('broadcast.urls')),
            # path('announcement/', include('announcements.urls')),
        ]
