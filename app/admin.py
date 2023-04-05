from django.contrib import admin
from .models import invoice_owner,user_profile

admin.site.register(invoice_owner)
admin.site.register(user_profile)