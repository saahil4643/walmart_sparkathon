from django.contrib import admin
from .models import Product
# Register your models here.


admin.site.register(Product)

# admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
