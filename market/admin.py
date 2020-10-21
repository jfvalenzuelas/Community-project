from django.contrib import admin
from .models import Category, Product, Image

# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model = Image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product

@admin.register(Image)
class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category)