import os
import django
import MySQLdb
from django.core.exceptions import ImproperlyConfigured

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cancer_herbs.settings')

try:
    django.setup()
except ImproperlyConfigured:
    pass

from herbs.models import Chemical, Plant, XRef

print("Starting.script...")

# Connect to your MySQL database
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="8nanyangdrive", db="cancer_herbs_database")

cursor = db.cursor()

print("Fetching data...")
# Fetch data from the Chemicals table
cursor.execute("SELECT * FROM Plants")
rows = cursor.fetchall()

print("Saving data...")
# Create a Chemicals instance for each row and save it to the Django database
for row in rows:
    plant = Plant(plant_id=row[0], taxonomy=row[1], ncbi_species_id=row[2], ncbi_subspecies_id=row[3])
    plant.save()
# Do the same for the Plants and XRef tables

db.close()

print("Script completed.")