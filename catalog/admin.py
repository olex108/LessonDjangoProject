from django.contrib import admin

from .models import Category, Product, Contacts, ClientMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    search_fields = ("name", "description")
    list_filter = ("category",)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone")


@admin.register(ClientMessage)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "message", "created_at", "is_answered")
    search_fields = ("name", "phone", "created_at", "is_answered")
    list_filter = ("is_answered",)
