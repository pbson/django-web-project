from django.contrib import admin
from .models import Category,Product,Order,OrderProduct,Address
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'address_1',
                    'address_2',
                    'get_total'
                    ]
    list_display_links = [
        'user',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',]
    search_fields = [
        'user__username',
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'default'
    ]
    list_filter = ['default']
    search_fields = ['user', 'street_address', 'apartment_address']



admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Address,AddressAdmin)







