from django.contrib import admin
from Eshop.models import Account, Address, Sale, Shoppingcar, Order, OrderItem
# Register your models here.

admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Sale)
admin.site.register(Shoppingcar)
admin.site.register(OrderItem)
admin.site.register(Order)
