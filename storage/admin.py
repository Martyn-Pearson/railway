from django.contrib import admin
from .models import Locomotive, Load, Train, Location, TrainLocomotive

# Register your models here.

class TrainLocoInline(admin.TabularInline):
    model = TrainLocomotive

class TrainAdmin(admin.ModelAdmin):
    inlines = [
        TrainLocoInline
    ]

admin.site.register(Locomotive)
admin.site.register(Load)
admin.site.register(Train, TrainAdmin)
admin.site.register(Location)