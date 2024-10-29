import os
import django
import pandas as pd
from django.core.management.base import BaseCommand
from climate.models import WaterUsage, IrrigationPlan, WaterSource  # Mettez à jour avec votre chemin d'importation correct
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriDjango.settings')  # Modifiez selon le nom de votre projet
django.setup()

import pandas as pd
from climate.models import WaterUsage, IrrigationPlan, WaterSource  # Mettez à jour avec votre chemin d'importation correct
class Command(BaseCommand):
    help = 'Importe les données d\'utilisation de l\'eau depuis un fichier CSV'

    def handle(self, *args, **kwargs):
        # Lire le fichier CSV
        data_file_path = 'climate/water_usage_data.csv'  # Mettez à jour le chemin si nécessaire
        df = pd.read_csv(data_file_path)

        # Importer les données dans la base de données
        for _, row in df.iterrows():
            irrigation_plan = IrrigationPlan.objects.get(id=row['irrigation_plan'])
            water_source = WaterSource.objects.get(id=row['water_source'])
            WaterUsage.objects.create(
                irrigation_plan=irrigation_plan,
                water_source=water_source,
                amount_used=row['amount_used']
            )

        self.stdout.write(self.style.SUCCESS('Données d\'utilisation de l\'eau importées avec succès!'))