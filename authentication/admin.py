from django.contrib import admin

from authentication.models import (
    User,
)
from common.utils import all_fields_names


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка User."""

    list_display = all_fields_names(User)
