"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app.authentication import views as auth_views
from .docs import schema_view

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', auth_views.AuthViewSet, basename='auth')
router.register('users', auth_views.UserViewSet, basename='user')
router.register('customers', auth_views.CustomerViewSet, basename='customer')
router.register('employees', auth_views.EmployeeViewSet, basename='employee')

urlpatterns = [
    path('api/', include(router.urls)),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework'),
    ),
    path('swagger/', schema_view.with_ui('swagger'), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc'), name='redoc'),
    path('admin/', admin.site.urls),
]
