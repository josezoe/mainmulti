# shared/geodata.py
import csv
import os
from django.conf import settings

def get_city_data(geoname_id):
    """
    Retrieve city data by geoname_id from the CSV file.

    Args:
    geoname_id (str): The geoname_id for which to fetch city data.

    Returns:
    dict: A dictionary containing city data or an empty dict if not found.
    """
    csv_path = os.path.join(settings.BASE_DIR, 'shared', 'Geocity', 'city.csv')
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['geoname_id'] == geoname_id:
                return row
    return {}

# If you need to perform multiple lookups, consider caching results or using database for speed.