from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from accounts.models import User, GroupDescription

# Unregistering the default Group admin to customize it
admin.site.unregister(Group)


# Register your models here.
class GroupDescriptionInline(admin.StackedInline):
    model = GroupDescription


@admin.register(Group)
class InternalGroupAdmin(GroupAdmin):
    inlines = [GroupDescriptionInline]


admin.site.register(User, UserAdmin)
