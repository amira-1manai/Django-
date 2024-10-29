import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import datetime
from .models import Field
from django.contrib import messages


def fetch_weather_data(request):
    city = request.GET.get('city')
    api_key = 'b698494103add4361a716425d3c81fca'
    
    # Get coordinates using OpenWeatherMap
    geocode_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(geocode_url).json()
    
    if response.get("cod") != 200:
        error_message = f"City '{city}' not found."
        return render(request, 'frontoffice/weather/weather-display.html', {'error': error_message, 'city': city})

    lat, lon = response['coord']['lat'], response['coord']['lon']
    
    # Fetch forecast from Open-Meteo
    open_meteo_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&timezone=auto'
    forecast_response = requests.get(open_meteo_url).json()

    # Preprocess forecast data
    forecast_data = []
    for date, max_temp, min_temp in zip(forecast_response['daily']['time'], forecast_response['daily']['temperature_2m_max'], forecast_response['daily']['temperature_2m_min']):
        forecast_data.append({
            'date': date,
            'max_temp': max_temp,
            'min_temp': min_temp,
        })

    return render(request, 'frontoffice/weather/weather-display.html', {'forecast_data': forecast_data, 'city': city})


def home_view(request):
    return render(request, 'frontoffice/layout/app.html')
def template_tables(request):
    return render(request, 'frontoffice/template/tables.html')


# Field views
def create_field(request):
    if request.method == 'POST':
        size = request.POST.get('size')
        location = request.POST.get('location')
        crop_type = request.POST.get('crop_type')
        soil_type = request.POST.get('soil_type')

        # Perform validation here (simple example)
        errors = {}
        if not size or not location or not crop_type or not soil_type:
            errors['field'] = 'All fields are required.'

        if not errors:
            Field.objects.create(size=size, location=location, crop_type=crop_type, soil_type=soil_type)
            return redirect('field_list')  # Redirect to list view

        # If there are errors, render the form again with errors
        return render(request, 'frontoffice/create_field.html', {'errors': errors})

    return render(request, 'frontoffice/field/create_field.html')

def field_list(request):
    fields = Field.objects.all()  # Fetch all field instances from the database
    return render(request, 'frontoffice/field/field_list.html', {'fields': fields})

def field_delete(request, field_id):
    field = get_object_or_404(Field, id=field_id)  # Fetch the field instance by ID
    if request.method == 'POST':
        field.delete()  # Delete the field
        messages.success(request, 'Field deleted successfully.')  # Success message
        return redirect('field_list')  # Redirect to the field list page
    return redirect('field_list')

def field_update(request, field_id):
    field = get_object_or_404(Field, id=field_id)

    if request.method == 'POST':
        field.size = request.POST['size']
        field.location = request.POST['location']
        field.crop_type = request.POST['crop_type']
        field.soil_type = request.POST['soil_type']
        field.save()
        return redirect('field_list')

    return render(request, 'frontoffice/field/update_field.html', {'field': field})