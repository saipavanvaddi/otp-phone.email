from django.contrib import admin
from .models import Apartment, ApartmentFlat, ApartmentVisitor

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_blocks', 'total_flats')
    search_fields = ('name', 'address')

@admin.register(ApartmentFlat)
class ApartmentFlatAdmin(admin.ModelAdmin):
    list_display = ('flat_number', 'apartment', 'block', 'flat_type', 'owner_name', 'status')
    list_filter = ('apartment', 'status', 'flat_type')
    search_fields = ('flat_number', 'owner_name', 'owner_email')

@admin.register(ApartmentVisitor)
class ApartmentVisitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'flat', 'purpose', 'created_at')
    list_filter = ('purpose', 'created_at')
    search_fields = ('name', 'contact_number')


