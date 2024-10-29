from django.urls import path
from .views import IrrigationPredictionView, index


urlpatterns = [
    path('', index, name='predict'),
    path('predict/', IrrigationPredictionView.as_view(), name='irrigation_prediction'),
]