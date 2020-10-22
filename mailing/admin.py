from django.contrib import admin

from mailing.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Информаионные рассылки."""
    list_display = ('name', 'subject', 'from_user', 'created')
    list_display_links = ('name',)
    list_filter = ('created',)
    search_fields = ('name', 'subject')
    save_on_top = True
