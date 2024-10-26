from django import forms
from .models import FertilizationSchedule

class FertilizationScheduleForm(forms.ModelForm):
    class Meta:
        model = FertilizationSchedule
        fields = ['crop', 'fertilizer_type', 'amount', 'application_date']
