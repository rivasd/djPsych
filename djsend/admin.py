from django.contrib import admin
# Register your models here.
from django_markdown.admin  import MarkdownModelAdmin
from django.apps import apps

app = apps.get_app_config('djsend')

for model_name, model in app.models.items():
    admin.site.register(model, MarkdownModelAdmin)
