from django.db import models

NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class Contacts(models.Model):
    """Модель контактов для звена сети по продаже электроники"""

    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    home = models.IntegerField(verbose_name='Номер дома')

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.home}\n{self.email}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    """Модель продукта для сети по продаже электроники"""

    title = models.CharField(max_length=100, verbose_name='Название')
    product_model = models.CharField(max_length=255, verbose_name='Модель продукта')
    reliz_date = models.DateField(verbose_name='Дата выхода')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.title} {self.product_model}'


class Link(models.Model):
    """Модель звена сети по продаже электроники"""

    title = models.CharField(max_length=100, verbose_name='Название')  # Название звена
    contacts = models.ForeignKey(Contacts, verbose_name='Контакты', on_delete=models.CASCADE)  # Контакты звена
    products = models.ManyToManyField(Product, verbose_name='Продукты')  # Продукты
    supplier = models.ForeignKey('self',
                                 verbose_name='Поставщик',
                                 on_delete=models.SET_NULL,
                                 **NULLABLE)  # Поставщик
    debt = models.DecimalField(max_digits=10,
                               decimal_places=2,
                               verbose_name='Задолженность',
                               **NULLABLE)  # задолженность перед поставщиком
    created_at = models.DateTimeField(auto_now_add=True)  # дата/время создания

    class Meta:
        verbose_name = 'Звено'
        verbose_name_plural = 'Звенья'

    def __str__(self):
        return self.title
