from django import forms
from django.core.validators import RegexValidator
from .models import ApartmentVisitor

class VisitorForm(forms.ModelForm):
    contact_number = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit contact number.')],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ApartmentVisitor
        fields = ['name', 'contact_number', 'flat', 'purpose', 'other_purpose', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'flat': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Select(attrs={'class': 'form-control'}),
            'other_purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }