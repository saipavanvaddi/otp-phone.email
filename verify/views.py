from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .user_data import get_user_data
from .models import  ApartmentVisitor, ApartmentFlat
from .forms import VisitorForm
from django.contrib import messages
from otp.supabase_config import supabase, BUCKET_NAME, STORAGE_URL
import base64
import uuid
from io import BytesIO
from django.utils import timezone

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
            # Validate required fields
            required_fields = ['name', 'flat', 'purpose', 'contact_number']
            for field in required_fields:
                if not request.POST.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'{field.replace("_", " ").title()} is required'
                    })

            # Get the ApartmentFlat instance
            flat_number = request.POST.get('flat')
            try:
                flat = ApartmentFlat.objects.get(flat_number=flat_number)
            except ApartmentFlat.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': f'Flat number {flat_number} does not exist'
                })
            
            # Handle photo upload to Supabase Storage
            photo_url = None
            photo_data = request.POST.get('photo')
            
            if photo_data:
                try:
                    # Remove the data URL prefix if present
                    if photo_data.startswith('data:image'):
                        photo_data = photo_data.split(',')[1]
                    
                    # Decode base64 to bytes
                    try:
                        photo_bytes = base64.b64decode(photo_data)
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid photo data format'
                        })
                    
                    # Generate a unique filename with timestamp
                    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{uuid.uuid4()}.jpg"
                    
                    # Upload to Supabase Storage
                    try:
                        # Upload file to the bucket
                        result = supabase.storage.from_(BUCKET_NAME).upload(
                            path=filename,
                            file=photo_bytes,
                            file_options={"content-type": "image/jpeg"}
                        )
                        
                        # Get the public URL using Supabase client
                        photo_url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
                        
                    except Exception as e:
                        print(f"Error uploading to Supabase: {str(e)}")  # Debug log
                        return JsonResponse({
                            'success': False,
                            'error': f'Failed to upload photo to storage: {str(e)}'
                        })
                        
                except Exception as e:
                    print(f"Error processing photo: {str(e)}")  # Debug log
                    return JsonResponse({
                        'success': False,
                        'error': f'Error processing photo: {str(e)}'
                    })
            
            # Validate purpose and other_purpose
            purpose = request.POST.get('purpose')
            other_purpose = request.POST.get('other_purpose')
            if purpose == 'Other' and not other_purpose:
                return JsonResponse({
                    'success': False,
                    'error': 'Please specify other purpose'
                })
            
            # Create visitor record with verified phone number and photo URL
            try:
                visitor = ApartmentVisitor.objects.create(
                    name=request.POST.get('name'),
                    contact_number=request.POST.get('contact_number'),
                    flat=flat,
                    purpose=purpose,
                    other_purpose=other_purpose if purpose == 'Other' else None,
                    photo_url=photo_url
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Visitor details saved successfully',
                    'visitor_id': visitor.id,
                    'photo_url': photo_url  # Return the photo URL in the response
                })
            except Exception as e:
                print(f"Error saving visitor: {str(e)}")  # Debug log
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to save visitor record: {str(e)}'
                })
                
        except Exception as e:
            print(f"Unexpected error: {str(e)}")  # Debug log
            return JsonResponse({
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })

def list_flats(request):
    flats = ApartmentFlat.objects.all()
    return render(request, 'list_flats.html', {'flats': flats})
