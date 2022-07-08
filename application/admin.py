from django.contrib import admin

from application import settings
from application.utils import mask_database_url_password


class ApplicationAdminSite(admin.AdminSite):
    site_header = 'Ingress CMS'

    def db_host(self):
        mongodb_url = mask_database_url_password(settings.MONGODB_URI)
        return f'{mongodb_url}/{settings.MONGODB_NAME}'

    def each_context(self, *args, **kwargs):
        context = super().each_context(*args, **kwargs)
        context["db_host"] = self.db_host()
        return context
