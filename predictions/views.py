from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import IrrigationPredictionSerializer
from .predictor import predict_irrigation

class IrrigationPredictionView(APIView):
    def post(self, request):
        serializer = IrrigationPredictionSerializer(data=request.data)
        if serializer.is_valid():
            prediction = predict_irrigation(serializer.validated_data)
            return Response({"irrigation_amount": prediction}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def index(request):
    prediction = None
    if request.method == "POST":
        temperature = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        rainfall = float(request.POST['rainfall'])
        soil_type = request.POST['soil_type'].capitalize()
        crop_type = request.POST['crop_type'].capitalize()
        
        inputs = {
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'soil_type': soil_type,
            'crop_type': crop_type,
        }
        prediction_amount = predict_irrigation(inputs)
        prediction = round(prediction_amount, 2) 

    return render(request, 'index.html', {'prediction': prediction})

