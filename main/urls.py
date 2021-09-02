from django.urls import path
from main import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('demo_site', views.demo_setting, name="setting"),
    path('demo_site/xss', views.demo_xss, name="demo_xss"),
    path('demo_site/sql', views.demo_sql, name="sql_demo"),
    path('demo_site/stored_xss', views.stored_xss, name="stored_xss"),
    path('demo_site/index', views.index, name="index"),
    path('demo_site/xss/output', views.xss_output, name="xss_output"),
    path('sql_api', views.sql_api, name="sql api"),
    path('xss_api', views.xss_api, name="xss api")
]