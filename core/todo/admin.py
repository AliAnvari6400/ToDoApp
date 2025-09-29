from django.contrib import admin
from .models import Task


class PostAdmin(admin.ModelAdmin):
    list_display = ["author", "title", "created_date", "updated_date"]


# Register your models here.
admin.site.register(Task)
