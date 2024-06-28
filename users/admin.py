from django.contrib import admin
from .models import User, Notification
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "date_joined"]
    list_per_page = 10
    list_filter = ["username"]
    search_fields = ["username", "department", "email", "first_name"]


admin.site.register(User, UserAdmin)
admin.site.register(Notification)

