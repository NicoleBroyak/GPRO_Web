from django.contrib import admin
from django.urls import path
from . import views
from gpro import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.current_datetime),
    ]