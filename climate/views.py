import requests
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
import datetime
from .models import Field
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Crop
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import FertilizationSchedule


import pickle
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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


def create_crop(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        water_requirement = request.POST.get('water_requirement')

        if name and water_requirement:
            try:
                water_requirement = float(water_requirement)
                Crop.objects.create(name=name, water_requirement=water_requirement)
                messages.success(request, 'Crop created successfully!')
                return redirect('crop_list')  # Redirigez vers une liste des crops ou une autre vue
            except ValueError:
                messages.error(request, 'Please enter a valid number for water requirement.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'frontoffice/crop/create_crop.html')


def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'frontoffice/crop/crop_list.html', {'crops': crops})


def crop_update(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    errors = {}
    
    if request.method == "POST":
        name = request.POST.get('name')
        water_requirement = request.POST.get('water_requirement')

        # Validation simple
        if not name:
            errors['crop'] = "Name is required."
        if not water_requirement:
            errors['crop'] = "Water requirement is required."

        if not errors:
            crop.name = name
            crop.water_requirement = float(water_requirement)
            crop.save()
            return redirect('crop_list')

    return render(request, 'frontoffice/crop/update_crop.html', {'crop': crop, 'errors': errors})


def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == "POST":
        crop.delete()
        return redirect('crop_list')
    return redirect('crop_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FertilizationSchedule, Crop

# Afficher la liste des programmes de fertilisation
def fertilization_list(request):
    schedules = FertilizationSchedule.objects.all()
    return render(request, 'frontoffice/fertilization/fertilization_list.html', {'schedules': schedules})

# Créer un programme de fertilisation
def create_fertilization(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        fertilizer_type = request.POST.get('fertilizer_type')
        amount = request.POST.get('amount')
        application_date = request.POST.get('application_date')

        # Validation des champs requis
        if not all([crop_id, fertilizer_type, amount, application_date]):
            messages.error(request, 'Tous les champs sont obligatoires.')
            crops = Crop.objects.all()
            return render(request, 'frontoffice/fertilization/create_fertilization.html', {'crops': crops})

        # Obtenir l'instance de Crop en fonction de l'ID fourni
        crop_instance = get_object_or_404(Crop, id=crop_id)

        # Créer l'objet FertilizationSchedule avec l'instance de Crop
        FertilizationSchedule.objects.create(
            crop=crop_instance,
            fertilizer_type=fertilizer_type,
            amount=amount,
            application_date=application_date
        )
        messages.success(request, 'Programme de fertilisation créé avec succès !')
        return redirect('fertilization_list')

    crops = Crop.objects.all()  # Passer la liste des cultures disponibles pour le formulaire
    return render(request, 'frontoffice/fertilization/create_fertilization.html', {'crops': crops})

# Mettre à jour un programme de fertilisation existant
def update_fertilization(request, fertilization_id):
    fertilization_schedule = get_object_or_404(FertilizationSchedule, id=fertilization_id)
    crops = Crop.objects.all()
    
    if request.method == 'POST':
        crop_id = request.POST.get('crop')
        fertilizer_type = request.POST.get('fertilizer_type')
        amount = request.POST.get('amount')
        application_date = request.POST.get('application_date')

        # Validation des champs requis
        if not all([crop_id, fertilizer_type, amount, application_date]):
            messages.error(request, 'Tous les champs sont obligatoires.')
            context = {
                'fertilization_schedule': fertilization_schedule,
                'crops': crops,
            }
            return render(request, 'frontoffice/fertilization/update_fertilization.html', context)

        # Effectuer la mise à jour
        fertilization_schedule.crop_id = crop_id
        fertilization_schedule.fertilizer_type = fertilizer_type
        fertilization_schedule.amount = amount
        fertilization_schedule.application_date = application_date
        fertilization_schedule.save()
        messages.success(request, 'Programme de fertilisation mis à jour avec succès !')
        return redirect('fertilization_list')  # rediriger vers la liste des fertilisations

    context = {
        'fertilization_schedule': fertilization_schedule,
        'crops': crops,
    }
    return render(request, 'frontoffice/fertilization/update_fertilization.html', context)

# Supprimer un programme de fertilisation
def delete_fertilization(request, schedule_id):
    schedule = get_object_or_404(FertilizationSchedule, id=schedule_id)
    if request.method == "POST":
        schedule.delete()
        messages.success(request, 'Programme de fertilisation supprimé avec succès !')
        return redirect('fertilization_list')
    return render(request, 'frontoffice/fertilization/delete_fertilization.html', {'schedule': schedule})














###############################
# Charger le modèle ML
with open('climate/fertilization_model.pkl', 'rb') as f:
    model = pickle.load(f)

@csrf_exempt  # Pour éviter les problèmes CSRF lors des tests
def predict_fertilization(request):
    if request.method == "POST":
        # Récupérer les données de la requête POST
        crop_type = int(request.POST.get('crop_type'))
        soil_type = int(request.POST.get('soil_type'))
        
        # Faire la prédiction
        prediction = model.predict([[crop_type, soil_type]])

        # Retourner la prédiction comme JSON
        return JsonResponse({'predicted_fertilizer_amount': prediction[0]})
    
    return render(request, 'frontoffice/fertilization/predict_fertilization.html')