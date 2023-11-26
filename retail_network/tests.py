from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from employee.models import Employee
from retail_network.models import Contacts, Product, Link


class LinkTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед запуском тестов"""

        # Создание сотрудника для тестирования
        self.employee = Employee.objects.create(email='test_user@test.ru',
                                                username='admin',
                                                is_staff=False,
                                                is_superuser=False,
                                                is_active=True)

        self.employee.set_password('qwerty')  # Устанавливаем пароль
        self.employee.save()  # Сохраняем изменения пользователя в базе данных

        # Запрос токена для авторизации
        response = self.client.post('/api/token/', data={'username': self.employee.username, 'password': 'qwerty'})
        self.access_token = response.data.get('access')  # Токен для авторизации

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)  # Авторизация пользователя

        # Создание контактов
        self.contacts = Contacts.objects.create(email='test@test.ru',
                                                country='Russia',
                                                city='SPb',
                                                street='Mira',
                                                home=17)

        # создание продукта
        self.product = Product.objects.create(title='Notebook',
                                              product_model='QR4598HD',
                                              reliz_date='2023-11-23')

        # создание звена
        self.plant = Link.objects.create(title='Acer_plant',
                                         contacts=self.contacts,
                                         )
        self.plant.products.set([self.product])

    def test_create_link(self):
        """Тестирование создания звена"""

        data = {'title': 'Acer_seller',
                'contacts': self.contacts.pk,
                'products': [self.product.pk],
                'supplier': self.plant.pk}

        response = self.client.post(reverse('retail-network:api-chain-create'), data=data)  # Отправка запроса

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверка статуса ответа
        self.assertEqual(Link.objects.all().count(), 2)  # Проверка наличия в базе данных новой записи

    def test_list_links(self):
        """Тестирование просмотра списка звеньев сети"""

        response = self.client.get(reverse('retail-network:api-chain-list'))  # Запрос на получение списка уроков

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка ответа на запрос

    def test_update_link(self):
        """Тестирование обновления данных о звене сети"""

        data = {'title': 'Acer_plant_update',
                'contacts': self.contacts.pk,
                'products': [self.product.pk],
                'supplier': self.plant.pk}

        response = self.client.put(reverse('retail-network:api-chain-update', args=[self.plant.pk]), data=data)
        self.plant.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа

        self.assertEqual(self.plant.title, 'Acer_plant_update')  # проверка обновился ли атрибут

    def test_destroy_link(self):
        """Тестирование удаления звена сети"""

        response = self.client.delete(reverse('retail-network:api-chain-destroy', args=[self.plant.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверка статуса ответа

        self.assertEqual(Link.objects.all().count(), 0)  # Проверка количества записей уроков в БД
