"""ingress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView

from ingress import settings

admin.site.site_header = 'Ingress CMS'


def mask_database_url_password(url: str) -> str:
    parts = url.split(":")
    assert len(parts) == 4
    parts = parts[2].split('@')
    assert len(parts) == 2
    password = parts[0]
    updated_url = url.replace(password, "***")
    assert url != updated_url
    return updated_url


def each_context(*args, **kwargs):
    context = original_each_context(*args, **kwargs)
    mongodb_url = mask_database_url_password(settings.MONGODB_URI)
    context['db_host'] = f'{mongodb_url}/{settings.MONGODB_NAME}'
    return context


original_each_context = admin.site.each_context
admin.site.each_context = each_context

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('admin/', admin.site.urls),
]
