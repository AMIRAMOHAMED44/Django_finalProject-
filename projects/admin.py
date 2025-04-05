from django.contrib import admin
from .models import Project, Category

admin.site.register(Project)
admin.site.register(Category)
# projects/admin.py

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
