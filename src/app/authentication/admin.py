import csv

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .models import CustomUser, Customer, Employee


# Register your models here.
def download_users_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Id', 'Role', 'Name', 'Last login', 'Date joined'])
    for user in queryset:
        writer.writerow([
            user.id,
            user.role,
            user.get_full_name(),
            user.last_login,
            user.date_joined,
        ])

    return response


download_users_csv.short_description = "Download selected users' CSV"


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 0


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'role'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    inlines = (CustomerInline, EmployeeInline)
    actions = (download_users_csv,)

    class Media:
        js = ('js/authentication/role.js',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')

    def full_name(self, obj):
        return obj.user.get_full_name()


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')

    def full_name(self, obj):
        return obj.user.get_full_name()
