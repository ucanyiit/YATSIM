from django.contrib import admin

from .models import Cell, Room, Train, Wagon

admin.site.register(Room)
admin.site.register(Cell)
admin.site.register(Train)
admin.site.register(Wagon)
