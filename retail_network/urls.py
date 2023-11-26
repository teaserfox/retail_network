from django.urls import path

from retail_network.apps import RetailNetworkConfig
from retail_network.views import (RetailChainView, RetailChainDetailView, clear_debt, ContactsListView, LinkListAPIView,
                                LinkCreateAPIView, LinkRetrieveAPIView, LinkDestroyAPIView, LinkUpdateAPIView,
                                ContactCreateAPIView, ProductCreateAPIView)

app_name = RetailNetworkConfig.name

urlpatterns = [
    path('', RetailChainView.as_view(), name='retail-chain-list'),  # главная страница со списком всех звеньев сети
    path('link/<int:pk>', RetailChainDetailView.as_view(), name='retail-network'),  # звено сети детально
    path('clear-debt/<int:pk>', clear_debt, name='clear-debt'),  # очистка долга перед поставщиком
    path('city-list', ContactsListView.as_view(), name='city-list'),  # список городов
    path('<int:pk>', RetailChainView.as_view(), name='retail-chain-city'),  # фильтр звеньев сети по городу
    path('api/links', LinkListAPIView.as_view(), name='api-chain-list'),  # список звеньев сети через API
    path('api/links/create', LinkCreateAPIView.as_view(), name='api-chain-create'),  # создание звена сети через API
    path('api/links/<int:pk>', LinkRetrieveAPIView.as_view(), name='api-chain'),  # звено сети детально через API
    path('api/links/delete/<int:pk>', LinkDestroyAPIView.as_view(), name='api-chain-destroy'),  # удаление звена API
    path('api/links/update/<int:pk>', LinkUpdateAPIView.as_view(), name='api-chain-update'),  # обновление звена API
    path('api/contacts/create', ContactCreateAPIView.as_view(), name='api-contact-create'),  # добавление контактов
    path('api/product/create', ProductCreateAPIView.as_view(), name='api-product-create'),  # добавление продукта
]