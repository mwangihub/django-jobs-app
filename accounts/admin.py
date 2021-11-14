from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.authentication.forms import UserAdminCreationForm, UserAdminChangeForm

from accounts import models as acc_db


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    search_fields = ["email", "first_name", "second_name"]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    # The fields to be used in displaying the CustomUser model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.CustomUser.'admin', 'active', 'staff', "first_name", "second_name",'id',
    list_display = (
        "email",
        "first_name",
        'id',
        #"colored_first_name",
        "second_name",
        "admin",
        "active",
        "staff",
        "buyer",
        "employee",
        'slug'
    )
    list_filter = ("admin", "active", "staff")
    fieldsets = (
        ("Basic", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "second_name", "slug")}),
        ("Permissions",{"fields": ("admin","active","staff", )},),
        ("Others",{"fields": ("buyer","employee",)},),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",),"fields": ("email","password1","password2","first_name",\
                    "second_name", "active","staff","admin","buyer","employee",),}, ),
    )
    ordering = ("email",)
    filter_horizontal = ()


class AdminInnovestMessages(admin.ModelAdmin):
    list_display = (
        "session_user",
        "names",
        "email",
        "inform_us",
        "created_at",
        "message",
    )


class AdminInnovestSubscribers(admin.ModelAdmin):
    list_display = ("email", "created_at", "subscribe")


class AdminThemes(admin.ModelAdmin):
    list_display = ("session", "light", "accent",)


class AdminEmployeeProfile(admin.ModelAdmin):
    list_display = (
        "user",
        "avatar",
        "gender",
        "phone",
        "created_at",
    )


class AdminStaffProfile(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "second_name",
        "avatar",
        "gender",
        "phone",
        "created_at",
    )


admin.site.site_title = "Innovest Administrator pannel"
admin.site.index_title = "Administrator pannel | Innovest"
admin.site.site_header = "Administrator pannel Dashboard | Innovest"
# admin.site.unregister(Group)
admin.site.register(acc_db.User, UserAdmin)
admin.site.register(acc_db.InnovestUsersMessages, AdminInnovestMessages)
admin.site.register(acc_db.InnovestSubcribers, AdminInnovestSubscribers)
admin.site.register(acc_db.EmployeeProfile, AdminEmployeeProfile)
admin.site.register(acc_db.StaffProfile, AdminStaffProfile)
admin.site.register(acc_db.Theme, AdminThemes)
