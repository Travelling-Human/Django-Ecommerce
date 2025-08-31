from django.contrib import admin

# Register your models here.
from .models import ProductCategory, Product, OrderItem

@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ("order", "product", "quantity", "price")
