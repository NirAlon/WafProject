from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, token_refresh

import DBwaf.logger
import DBwaf.user
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api/logger/getlogger', DBwaf.logger.api_get_logger, name="api logger"),
    path('export_logger_csv/', DBwaf.logger.export_logger_csv, name="export"),
    path('logger/', DBwaf.logger.logger_page, name='logger'),
    path('login/', DBwaf.user.login_page, name='login'),
    path('logout/', DBwaf.user.logoutpage, name='logout'),
    path('change_password/', DBwaf.user.change_password_anno, name='change_pass'),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]