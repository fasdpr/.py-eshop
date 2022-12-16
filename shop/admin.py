from django.contrib import admin

from .models import Product,Category,OrderItem,Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','price','updated']
    prepopulated_fields={'slug':('name',)}
    list_filter=('available','created','updated')
    list_editable=('price',)
    
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    raw_id_fields=('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','updated','paid']    
    list_filter=('paid',)
    inlines=(OrderItemInline,)