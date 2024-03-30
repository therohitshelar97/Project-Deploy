from django.contrib import admin
from .models import Animals,Order_History,Order

# Register your models here.
admin.site.register(Animals)
admin.site.register(Order_History)

@admin.register(Order)
class OrderData(admin.ModelAdmin):
    display_list = ['id','user','animals','addres','order_id','payment','delivery_date']

# @admin.register(Order_History)
# class OrderHistory(admin.ModelAdmin):
#     display_list = ['pname']
