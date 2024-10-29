from django.contrib import admin

from .models import Field, IrrigationPlan, Crop, WaterSource, WeatherData, FertilizationSchedule
from .models import Field, IrrigationPlan, Crop, WaterSource, WeatherData,WaterUsage

admin.site.register(Field)
admin.site.register(IrrigationPlan)
admin.site.register(Crop)
admin.site.register(WaterSource)
admin.site.register(WeatherData)
admin.site.register(FertilizationSchedule)
admin.site.register(WaterUsage)

