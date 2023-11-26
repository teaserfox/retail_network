from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employee.models import Employee

admin.site.register(Employee, UserAdmin)  # регистрация модели Employee в админ-панели
