from django.contrib import admin
from .models import Artist, Album, Track

# Basic admin registration without type hints
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
