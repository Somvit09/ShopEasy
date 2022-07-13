from django.contrib import admin
from .models import Product, VariationModel


# Register your models here.

class ModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active',)
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active',)


admin.site.register(Product, ModelAdmin)
admin.site.register(VariationModel, VariationAdmin)
