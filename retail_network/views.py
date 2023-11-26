from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from retail_network.models import Link, Contacts
from retail_network.serializers import LinkSerializer, ContactSerializer, ProductSerializer


class RetailChainView(ListView):
    """Класс-контроллер для отображения главной страницы"""

    model = Link  # Модель
    template_name = 'retail_network/retail_network.html'  # шаблон

    def get_queryset(self, *args, **kwargs):
        """Переопределение метода для формирования списка нужного списка звеньев сети"""

        queryset = []  # изначальный список

        # если пользователь авторизован
        if not self.request.user.is_anonymous:
            pk = self.kwargs.get('pk')  # проверяем есть ли в аргументах pk(ссылка на контакты)
            queryset = Link.objects.all()  # наполняем список звеньев сети

            # если в аргументах есть pk
            if pk:

                city = Contacts.objects.get(pk=pk).city  # по переданному pk находим город
                new_queryset = [link for link in queryset if link.contacts.city == city] # фильтруем список по городу
                queryset = new_queryset  # перезаписываем список звеньев сети

        return queryset


class RetailChainDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для отображения страницы с информацией о звене сети"""
    model = Link  # модель
    template_name = 'retail_network/link_detail.html'  # шаблон


@login_required
def clear_debt(request, pk):
    """контроллер для обнуления задолженности перед поставщиком"""

    link = Link.objects.get(pk=pk)  # получаем нужное звено сети
    link.debt = 0  # обнуляем задолженность перед поставщиком
    link.save()  # сохраняем результат

    return redirect(reverse('retail-network:retail-chain-list'))  # перенаправляем на главную страницу


class ContactsListView(LoginRequiredMixin, ListView):
    """Контроллер для отображения списка городов"""

    model = Contacts  # Модель
    template_name = 'retail_network/contacts-list.html'  # шаблон

    def get_queryset(self):
        """переопределяем метод для создания списка контактов с уникальными городами"""

        contacts = Contacts.objects.all()  # список всех контактов
        queryset = []  # пустой список контактов
        cities = []  # пустой список городов

        for contact in contacts:

            # если города еще нет в списке
            if contact.city not in cities:
                cities.append(contact.city)  # добавляем город в список городов
                queryset.append(contact)  # добавляем контакты в список контактов

        return queryset


class LinkListAPIView(generics.ListAPIView):
    """Контроллер для просмотра списка звеньев сети через API"""

    serializer_class = LinkSerializer  # Сериализатор
    queryset = Link.objects.all()  # список звеньев сети

    permission_classes = [IsAuthenticated]  # разрешение на доступ авторизованным пользователям

    filter_backends = [filters.SearchFilter]  # фильтр
    search_fields = ['contacts__country']  # поле фильтрации по стране


class LinkCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания звена сети"""

    serializer_class = LinkSerializer  # сериализатор
    permission_classes = [IsAuthenticated]  # разрешение на доступ авторизованным пользователям


class LinkRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра звена сети"""

    serializer_class = LinkSerializer  # сериализатор
    queryset = Link.objects.all()  # список звеньев сети

    permission_classes = [IsAuthenticated]  # разрешение на доступ авторизованным пользователям


class LinkDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления звена сети"""

    queryset = Link.objects.all()  # список звеньев сети

    permission_classes = [IsAuthenticated]  # разрешение на доступ авторизованным пользователям


class LinkUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения звена сети"""

    serializer_class = LinkSerializer  # сериализатор
    queryset = Link.objects.all()  # список звеньев сети
    permission_classes = [IsAuthenticated]  # разрешение на доступ авторизованным пользователям

    def perform_update(self, serializer):
        """Удаляем поле debt из обновляемых данных"""

        debt = serializer.validated_data.pop('debt', None)  # удаление поля
        serializer.save()  # сохранение обновленных данных


class ContactCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания контактов"""

    serializer_class = ContactSerializer  # сериализатор
    permission_classes = [IsAuthenticated]  # разрешение на доступ для авторизованных пользователей


class ProductCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания продукта"""

    serializer_class = ProductSerializer  # Сериализатор
    permission_classes = [IsAuthenticated]

