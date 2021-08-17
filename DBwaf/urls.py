"""DBwaf URL Configuration

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

import DBwaf.logger
import DBwaf.user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('export_logger_csv/', DBwaf.logger.export_logger_csv, name="export"),
    path('logger/', DBwaf.logger.logger_page, name='logger'),
    path('login/', DBwaf.user.login_page, name='login'),
    path('logout/', DBwaf.user.user_logout, name='logout'),
    path('change_password/', DBwaf.user.change_password_anno, name='change_pass'),

]