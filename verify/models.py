from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password

# Create your models here.

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
        ('Family/Friend', 'Family/Friend'),
        ('Delivery', 'Delivery'),
        ('Maintenance', 'Maintenance'),
        ('Service', 'Service'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    contact_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit contact number')]
    )
    flat_number = models.CharField(max_length=50)  # Keep the old field temporarily
    flat = models.ForeignKey('ApartmentFlat', on_delete=models.CASCADE, related_name='visitors', null=True)  # Add null=True temporarily
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    other_purpose = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='visitor_photos/', blank=True, null=True)
    visit_date = models.DateField(default=timezone.now)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(blank=True, null=True)
    is_checked_out = models.BooleanField(default=False)
    action = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        flat_display = self.flat.flat_number if self.flat else self.flat_number
        return f"{self.name} - Visiting {flat_display} on {self.visit_date.strftime('%Y-%m-%d')} at {self.check_in_time.strftime('%H:%M')}"
