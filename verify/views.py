from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .user_data import get_user_data
from .models import  ApartmentVisitor, ApartmentFlat
from .forms import VisitorForm
from django.contrib import messages

# Create your views here.

def index(request):
    # Get all flat numbers for the dropdown
    flat_numbers = ApartmentFlat.objects.values_list('flat_number', flat=True)
    
    # Render the index page with flat numbers
    response = render(request, 'index.html', {'flat_numbers': flat_numbers})
    
    # Set the Cross-Origin-Opener-Policy header for handling popups
    response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response

def success(request):
    return render(request, 'success.html')

def get_user_info(request):
    user_json_url = request.GET.get('user_json_url')
    
    if not user_json_url:
        return JsonResponse({'error': 'Missing user_json_url parameter'})
    
    try:
        # Fetch user data from phone.email API
        response = requests.get(user_json_url)
        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch user data'})
        
        user_data = response.json()
        
        # Extract phone number from the API response
        phone_number = user_data.get('user_phone_number', '')
        
        # Return success response with phone number
        return JsonResponse({
            'success': True,
            'phone_number': phone_number
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)})

def save_visitor(request):
    if request.method == 'POST':
        try:
            # Get the ApartmentFlat instance
            flat_number = request.POST.get('flat')
            flat = ApartmentFlat.objects.get(flat_number=flat_number)
            
            # Create visitor record with verified phone number
            visitor = ApartmentVisitor.objects.create(
                name=request.POST.get('name'),
                contact_number=request.POST.get('contact_number'),  # This comes from OTP verification
                flat=flat,  # Pass the ApartmentFlat instance
                purpose=request.POST.get('purpose'),
                other_purpose=request.POST.get('other_purpose'),
                photo=request.FILES.get('photo')
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Visitor details saved successfully'
            })
        except ApartmentFlat.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid flat number'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })

def list_flats(request):
    flats = ApartmentFlat.objects.all()
    return render(request, 'list_flats.html', {'flats': flats})
