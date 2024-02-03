from django.contrib import admin
from . models import Category, Products
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products)
