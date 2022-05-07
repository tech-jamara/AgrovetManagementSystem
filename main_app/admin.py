from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(CustomUser)

admin.site.register(SysAdmin)
admin.site.register(Veterinarian)
admin.site.register(Customer)
admin.site.register(New_stock)
admin.site.register(Stock_puchases)
admin.site.register(Supplier)
admin.site.register(Stock_category)
admin.site.register(PurchaseBill)
admin.site.register(CustomerItemsales)
admin.site.register(CustomerOrderItem)
admin.site.register(Appointment)






