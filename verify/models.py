from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Create your models here.

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_blocks = models.IntegerField(default=1)
    total_flats = models.IntegerField()
    amenities = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ApartmentFlat(models.Model):
    PURPOSE_CHOICES = [
        ('Rental', 'Rental'),
        ('Owned', 'Owned'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Occupied', 'Occupied'),
        ('Maintenance', 'Maintenance'),
    ]

    FLAT_TYPES = [
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('2.5BHK', '2.5 BHK'),
        ('3BHK', '3 BHK'),
        ('3.5BHK', '3.5 BHK'),
        ('4BHK', '4 BHK'),
        ('Studio', 'Studio'),
    ]

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='flats')
    block = models.CharField(max_length=10, blank=True, null=True)
    flat_number = models.CharField(max_length=10)
    flat_type = models.CharField(max_length=10, choices=FLAT_TYPES)
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=15)
    owner_email = models.EmailField()
    flat_size = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')
    parking_slots = models.IntegerField(default=1)
    password = models.CharField(max_length=128)  # Added for authentication
    role = models.CharField(max_length=128, default='owner')

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Flat {self.flat_number}"

class ApartmentVisitor(models.Model):
    PURPOSE_CHOICES = [
        ('Personal', 'Personal Visit'),
        ('Delivery', 'Delivery'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    flat = models.ForeignKey(ApartmentFlat, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    other_purpose = models.CharField(max_length=100, blank=True, null=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)  # Store Supabase Storage URL
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)  # For visitor's location
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)  # For visitor's location
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Flat {self.flat.flat_number}"
