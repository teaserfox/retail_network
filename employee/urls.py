from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from employee.apps import EmployeeConfig

app_name = EmployeeConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='employee/login.html'), name='login'),  # вход в систему
    path('logout/', LogoutView.as_view(), name='logout'),  # выход из системы
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # получение токена для авторизации
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновление токена для авторизации
]