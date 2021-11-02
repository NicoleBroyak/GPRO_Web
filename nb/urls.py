from django.contrib import admin, auth
from django.urls import path
from django.conf.urls import include, url
from gpro import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('gpro_main', views.gpro_main),
    ]