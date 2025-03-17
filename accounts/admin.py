from django.contrib import admin
from .models import CustomUser, Parking, Reservation, Review

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type']
    list_filter = ['user_type']
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Parking)
admin.site.register(Reservation)
admin.site.register(Review)



