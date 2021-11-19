from django.contrib import admin
from .models import Track, Race, Season

admin.site.register(Race)
admin.site.register(Track)
admin.site.register(Season)