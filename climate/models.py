from django.db import models

# Irrigation Field
class Field(models.Model):
    size = models.FloatField()
    location = models.CharField(max_length=255)
    crop_type = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)

    def __str__(self):
        return f"Field {self.id} - {self.location}"

# Irrigation Plan Model
class IrrigationPlan(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    water_amount = models.FloatField()
    irrigation_date = models.DateTimeField()

    def __str__(self):
        return f"Irrigation Plan for Field {self.field.id} on {self.irrigation_date}"

# Crop Model
class Crop(models.Model):
    name = models.CharField(max_length=100)
    water_requirement = models.FloatField()

    def __str__(self):
        return self.name

# Water Source Model
class WaterSource(models.Model):
    type = models.CharField(max_length=100)
    capacity = models.FloatField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"Water Source {self.type} - {self.location}"

# Weather Data Model
class WeatherData(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    rainfall = models.FloatField()
    humidity = models.FloatField()

    def __str__(self):
        return f"Weather on {self.date} - Temp: {self.temperature}°C"




#FertilizationSchedule model 
class FertilizationSchedule(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    fertilizer_type = models.CharField(max_length=100)
    amount = models.FloatField()  # en kg/hectare, par exemple
    application_date = models.DateField()

    def __str__(self):
        return f"{self.fertilizer_type} pour {self.crop.name} le {self.application_date}"


