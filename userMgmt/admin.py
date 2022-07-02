from curses.ascii import US
from django.contrib import admin

from .models import User, Designation

# Register your models here.

admin.site.register(User)
admin.site.register(Designation)