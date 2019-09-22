from django.contrib import admin

# Register your models here.
from .models import product,Contact,order,updateorder

admin.site.register(product)
admin.site.register(Contact)
admin.site.register(order)
admin.site.register(updateorder)