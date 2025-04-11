import csv
from .models import *

def import_cities(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            print(row['city'], row['address'])
            Cities.objects.create(
                city=row['city'],
                adress=row['address'],
            )
