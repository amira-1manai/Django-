import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from .models import Field
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import IrrigationPlan  # Adjust the import based on your project structure
from .models import WaterSource  # Adjust the import path if needed
from .models import WaterUsage  # Adjust the import path if needed

def index(request):
    api_key = 'b698494103add4361a716425d3c81fca'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    city = request.GET.get('city')

    if not city:
        return JsonResponse({'error': 'City parameter is missing'})

    weather_data, daily_forecasts = fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url)

    return JsonResponse({
        'weather_data': weather_data,
        'daily_forecasts': daily_forecasts,
    })

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # Print the API response to inspect the structure
    print("Current weather response:", response)

    if 'coord' not in response:
        return {'error': f"City '{city}' not found or API error."}, []

    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    print("Forecast response:", forecast_response)

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    if 'daily' in forecast_response:
        for daily_data in forecast_response['daily'][:5]:
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
                'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
            })
    else:
        return {'error': 'Forecast data not available.'}, []

    return weather_data, daily_forecasts



def home_view(request):
    return render(request, 'frontoffice/layout/app.html')
def template_tables(request):
    return render(request, 'frontoffice/template/tables.html')


# fields
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

# Create a new water source
def create_water_source(request):
    if request.method == 'POST':
        type_ = request.POST.get('type')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity')

        errors = {}
        if not type_ or not location or not capacity:
            errors['field'] = 'All fields are required.'

        if not errors:
            WaterSource.objects.create(type=type_, location=location, capacity=capacity)
            return redirect('water_source_list')

        return render(request, 'frontoffice/water_sources/create_water_source.html', {'errors': errors})

    return render(request, 'frontoffice/water_sources/create_water_source.html')

# List all water sources
def water_source_list(request):
    water_sources = WaterSource.objects.all()
    return render(request, 'frontoffice/water_sources/water_source_list.html', {'water_sources': water_sources})

# Delete a water source
def water_source_delete(request, water_source_id):
    water_source = get_object_or_404(WaterSource, id=water_source_id)
    if request.method == 'POST':
        water_source.delete()
        messages.success(request, 'Water source deleted successfully.')
        return redirect('water_source_list')
    return redirect('water_source_list')

# Update a water source
def water_source_update(request, water_source_id):
    water_source = get_object_or_404(WaterSource, id=water_source_id)

    if request.method == 'POST':
        water_source.type = request.POST['type']
        water_source.location = request.POST['location']
        water_source.capacity = request.POST['capacity']
        water_source.save()
        return redirect('water_source_list')

    return render(request, 'frontoffice/water_sources/update_water_source.html', {'water_source': water_source})

# Create a new water usage
def create_water_usage(request):
    if request.method == 'POST':
        irrigation_plan_id = request.POST.get('irrigation_plan')
        water_source_id = request.POST.get('water_source')
        amount_used = request.POST.get('amount_used')

        errors = {}
        if not irrigation_plan_id or not water_source_id or not amount_used:
            errors['field'] = 'All fields are required.'

        if not errors:
            WaterUsage.objects.create(
                irrigation_plan_id=irrigation_plan_id,
                water_source_id=water_source_id,
                amount_used=amount_used
            )
            messages.success(request, 'Water usage created successfully.')
            return redirect('water_usage_list')

        return render(request, 'frontoffice/water_usages/create_water_usage.html', {
            'errors': errors,
            'irrigation_plans': IrrigationPlan.objects.all(),
            'water_sources': WaterSource.objects.all()
        })

    return render(request, 'frontoffice/water_usages/create_water_usage.html', {
        'irrigation_plans': IrrigationPlan.objects.all(),
        'water_sources': WaterSource.objects.all()
    })


# List all water usages
def water_usage_list(request):
    water_usages = WaterUsage.objects.all()
    return render(request, 'frontoffice/water_usages/water_usage_list.html', {
        'water_usages': water_usages
    })


# Update a water usage
def water_usage_update(request, water_usage_id):
    water_usage = get_object_or_404(WaterUsage, id=water_usage_id)

    if request.method == 'POST':
        water_usage.irrigation_plan_id = request.POST['irrigation_plan']
        water_usage.water_source_id = request.POST['water_source']
        water_usage.amount_used = request.POST['amount_used']
        water_usage.save()
        messages.success(request, 'Water usage updated successfully.')
        return redirect('water_usage_list')

    return render(request, 'frontoffice/water_usages/update_water_usage.html', {
        'water_usage': water_usage,
        'irrigation_plans': IrrigationPlan.objects.all(),
        'water_sources': WaterSource.objects.all()
    })
# Delete a water usage
def water_usage_delete(request, water_usage_id):
    water_usage = get_object_or_404(WaterUsage, id=water_usage_id)
    if request.method == 'POST':
        water_usage.delete()
        messages.success(request, 'Water usage deleted successfully.')
        return redirect('water_usage_list')
    return redirect('water_usage_list')  # Redirect if method is not POST