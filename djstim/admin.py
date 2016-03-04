from django.contrib import admin
from .models import *
# Register your models here.
# TODO: create the admin interface for the stimuli objects
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass