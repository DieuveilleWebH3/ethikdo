from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'account_type', 'gender'] 
    search_fields = ['username', 'email' ]
    list_filter = ['account_type', 'gender', ]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type: set[str]

        if not is_superuser:
            disabled_fields |= {
                'user',
                'is_superuser',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


