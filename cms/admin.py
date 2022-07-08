import json
from typing import List

from devtools import debug
from django import forms
from django.contrib import admin
from django.forms import widgets
from djongo.models import Field, JSONField

from cms.models import Bootstrap, Client, Configuration, GroupKey, Ticket


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'app_id')
    search_fields = list_display


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            as_str = json.dumps(value, indent=2, sort_keys=True)
            row_lengths = [len(row) for row in as_str.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            self.attrs['style'] = 'font-family: monospace'
            return as_str
        except Exception as e:
            debug("Error while formatting JSON", e)
            return super().format_value(dict(value))


class NestedFieldsCleanerMixin:
    def find_fields(self, field_model: Field) -> List[str]:
        return [
            name
            for _, name in filter(
                lambda pair: pair[0],
                [
                    (isinstance(field, field_model), field.name)
                    for field in self._meta.model._meta.fields
                ],
            )
        ]

    def clean(self):
        fields = self.find_fields(JSONField)
        for field in fields:
            self.cleaned_data[field] = json.loads(self.cleaned_data[field])
        return self.cleaned_data


class TicketAdminForm(NestedFieldsCleanerMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'


class OverrideJSON:
    formfield_overrides = {JSONField: {'widget': PrettyJSONWidget}}


@admin.register(Ticket)
class TicketAdmin(OverrideJSON, admin.ModelAdmin):
    form = TicketAdminForm

    list_display = ('user_id', 'group_id', 'display_name')
    search_fields = list_display


class ConfigurationAdminForm(NestedFieldsCleanerMixin, forms.ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'


@admin.register(Configuration)
class ConfigurationAdmin(OverrideJSON, admin.ModelAdmin):
    form = ConfigurationAdminForm

    list_display = ('client_id',)
    search_fields = list_display


class BootstrapAdminForm(NestedFieldsCleanerMixin, forms.ModelForm):
    class Meta:
        model = Bootstrap
        fields = '__all__'


@admin.register(Bootstrap)
class BootstrapAdmin(OverrideJSON, admin.ModelAdmin):
    form = BootstrapAdminForm

    list_display = ('client_id',)
    search_fields = list_display


@admin.register(GroupKey)
class GroupKeyAdmin(OverrideJSON, admin.ModelAdmin):
    list_display = ('group_key', 'group_id')
    search_fields = list_display
