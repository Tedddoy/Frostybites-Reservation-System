from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Services)
admin.site.register(Transaction)
admin.site.register(Reservation)