import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Crop
from .models import FertilizationSchedule
import pickle
from django.views.decorators.csrf import csrf_exempt
from .models import Field, IrrigationPlan, WaterSource, WaterUsage, Machine
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def fetch_weather_data(request):
    city = request.GET.get('city')
    api_key = 'b698494103add4361a716425d3c81fca'
    
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

        errors = {}
        if not size or not location or not crop_type or not soil_type:
            errors['field'] = 'All fields are required.'

        if not errors:
            Field.objects.create(size=size, location=location, crop_type=crop_type, soil_type=soil_type)
            return redirect('field_list')

        return render(request, 'frontoffice/create_field.html', {'errors': errors})

    return render(request, 'frontoffice/field/create_field.html')

def field_list(request):
    fields = Field.objects.all()
    return render(request, 'frontoffice/field/field_list.html', {'fields': fields})

def field_delete(request, field_id):
    field = get_object_or_404(Field, id=field_id)
    if request.method == 'POST':
        field.delete()
        messages.success(request, 'Field deleted successfully.')
        return redirect('field_list')
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
            messages.success(request, 'L\'utilisation de l\'eau a été créée avec succès.')
            return redirect('water_usage_list')

        return render(request, 'frontoffice/water_usages/create_water_usage.html', {
            'errors': errors,
            'irrigation_plans': IrrigationPlan.objects.all(),
            'water_sources': WaterSource.objects.all()
        })

    # GET request
    return render(request, 'frontoffice/water_usages/create_water_usage.html', {
        'irrigation_plans': IrrigationPlan.objects.all(),
        'water_sources': WaterSource.objects.all()
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
    return redirect('water_usage_list')

# List all water usages
def water_usage_list(request):
    water_usages = WaterUsage.objects.all()
    return render(request, 'frontoffice/water_usages/water_usage_list.html', {
        'water_usages': water_usages
    })
    
    
#
def train_and_predict(request):
    # Récupérer les données de WaterUsage
    data = pd.DataFrame(list(WaterUsage.objects.all().values()))

    # Ajoute ceci pour inspecter les données
    print(data.head())  # Affiche les 5 premières lignes du DataFrame dans la console

    if data.empty:
        return render(request, 'frontoffice/water_usages/predict.html', {'error': 'No data available for training.'})

    # Assurez-vous que les noms de colonnes correspondent à ceux dans le DataFrame
    if 'irrigation_plan_id' not in data.columns or 'water_source_id' not in data.columns:
        return render(request, 'frontoffice/water_usages/predict.html', {'error': 'Expected columns not found in data.'})

    # Encodage des variables catégorielles
    label_encoder = LabelEncoder()
    data['irrigation_plan'] = label_encoder.fit_transform(data['irrigation_plan_id'])
    data['water_source'] = label_encoder.fit_transform(data['water_source_id'])

    # Séparation des features et de la target
    X = data[['irrigation_plan', 'water_source']]
    y = data['amount_used']

    # Division en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Création du modèle
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Prédictions
    predictions = model.predict(X_test)

    # Convertir les prédictions en une liste pour le template
    predictions_list = predictions.tolist()

    # Renvoie le résultat au template
    return render(request, 'frontoffice/water_usages/predict.html', {'predictions': predictions_list})



def predict_water_usage(request):
    predicted_usage = None
    water_sources = WaterSource.objects.all()  # Fetch all water sources for the dropdown

    if request.method == 'POST':
        water_source_id = request.POST.get('water_source_id')
        water_source = get_object_or_404(WaterSource, id=water_source_id)

        # Load the trained model
        with open('climate/water_optimization_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Make a prediction using the capacity of the selected water source
        predicted_usage = model.predict([[water_source.capacity]])[0]

    return render(request, 'frontoffice/water_usages/predict_water_usage.html', {
        'predicted_usage': predicted_usage,
        'water_sources': water_sources,
    })

# Function to load your pre-trained model
def load_model():
    with open('climate/water_quality_model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

# View function for predicting water quality
def predict_water_quality_view(request):
    result = None  # Initialize result to None

    if request.method == 'POST':
        # Extracting values from the submitted form
        try:
            electrical_conductivity = float(request.POST.get('electrical_conductivity'))
            ph = float(request.POST.get('ph'))
            sar = float(request.POST.get('sar'))
            turbidity = float(request.POST.get('turbidity'))
            hardness = float(request.POST.get('hardness'))
            tds = float(request.POST.get('tds'))
            chloride = float(request.POST.get('chloride'))
            sulfate = float(request.POST.get('sulfate'))
            nitrate = float(request.POST.get('nitrate'))

            # Call the prediction function
            result = predict_water_quality(electrical_conductivity, ph, sar, turbidity, hardness, tds, chloride, sulfate, nitrate) # type: ignore

        except ValueError:
            result = "Please ensure all input values are valid numbers."

    return render(request, 'frontoffice/water_sources/water_quality_form.html', {'result': result})

# Prediction function
def predict_water_quality_view(request):
    result = None  # Initialize result to None

    if request.method == 'POST':
        # Extracting values from the submitted form
        try:
            electrical_conductivity = float(request.POST.get('electrical_conductivity'))
            ph = float(request.POST.get('ph'))
            sar = float(request.POST.get('sar'))
            turbidity = float(request.POST.get('turbidity'))
            hardness = float(request.POST.get('hardness'))
            tds = float(request.POST.get('tds'))
            chloride = float(request.POST.get('chloride'))
            sulfate = float(request.POST.get('sulfate'))
            nitrate = float(request.POST.get('nitrate'))

            # Load the model
            model = load_model()

            # Prepare the input data as a DataFrame
            input_data = pd.DataFrame({
                'Electrical_Conductivity_uS': [electrical_conductivity],
                'pH': [ph],
                'Sodium_Adsorption_Ratio': [sar],
                'Turbidity_NTU': [turbidity],
                'Hardness_mg_L': [hardness],
                'Total_Dissolved_Solids_mg_L': [tds],
                'Chloride_mg_L': [chloride],
                'Sulfate_mg_L': [sulfate],
                'Nitrate_mg_L': [nitrate]
            })

            # Make the prediction
            prediction = model.predict(input_data)

            # Interpret the prediction
            if prediction[0] == "Suitable":
                result = "The water quality is suitable for irrigation."
            else:
                result = "The water quality is not suitable for irrigation."

        except ValueError:
            result = "Please ensure all input values are valid numbers."

    # Render the template with the result
    return render(request, 'frontoffice/water_sources/water_quality_form.html', {'result': result})



# Create Machine View
def create_machine(request):
    fields = Field.objects.all()  # Get all fields for assignment
    if request.method == 'POST':
        name = request.POST.get('name')
        machine_type = request.POST.get('type')
        purchase_date = request.POST.get('purchase_date')
        last_maintenance_date = request.POST.get('last_maintenance_date')
        field_id = request.POST.get('field')  # Retrieve the field assignment if any

        errors = {}
        if not name or not machine_type or not purchase_date:
            errors['machine'] = 'Name, type, and purchase date are required fields.'

        # Only create the machine if there are no errors
        if not errors:
            field = Field.objects.get(id=field_id) if field_id else None
            Machine.objects.create(
                name=name,
                type=machine_type,
                purchase_date=purchase_date,
                last_maintenance_date=last_maintenance_date,
                field=field
            )
            messages.success(request, 'Machine created successfully.')
            return redirect('machine_list')

        return render(request, 'frontoffice/machine/create_machine.html', {'errors': errors, 'fields': fields})

    return render(request, 'frontoffice/machine/create_machine.html', {'fields': fields})

# List Machines View
def machine_list(request):
    machines = Machine.objects.all()
    return render(request, 'frontoffice/machine/machine_list.html', {'machines': machines})

# Delete Machine View
def machine_delete(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        machine.delete()
        messages.success(request, 'Machine deleted successfully.')
        return redirect('machine_list')
    return redirect('machine_list')

# Update Machine View
def machine_update(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    fields = Field.objects.all()  # Include fields for reassignment if needed

    if request.method == 'POST':
        machine.name = request.POST['name']
        machine.type = request.POST['type']
        machine.purchase_date = request.POST['purchase_date']
        machine.last_maintenance_date = request.POST.get('last_maintenance_date')
        field_id = request.POST.get('field')
        
        # Update the field assignment
        machine.field = Field.objects.get(id=field_id) if field_id else None
        machine.save()
        messages.success(request, 'Machine updated successfully.')
        return redirect('machine_list')

    return render(request, 'frontoffice/machine/update_machine.html', {'machine': machine, 'fields': fields})