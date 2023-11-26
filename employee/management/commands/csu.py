from django.core.management import BaseCommand

from employee.models import Employee


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        """Команда для создания суперпользователя"""
        employee = Employee.objects.create(email='admin@admin.ru',
                                           username='admin',
                                           first_name='admin',
                                           last_name='admin',
                                           is_staff=True,
                                           is_superuser=True)

        employee.set_password('admin')
        employee.save()
