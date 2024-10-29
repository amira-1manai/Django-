from rest_framework import serializers

class IrrigationPredictionSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    rainfall = serializers.FloatField()
    soil_type = serializers.ChoiceField(choices=['Clay', 'Loam', 'Sandy', 'Silty'])
    crop_type = serializers.ChoiceField(choices=['Wheat', 'Corn', 'Soybean', 'Rice', 'Cotton'])