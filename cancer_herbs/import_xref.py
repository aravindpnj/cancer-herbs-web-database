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
cursor.execute("SELECT * FROM XRef")
rows = cursor.fetchall()

print("Saving data...")
# Create a Chemicals instance for each row and save it to the Django database
for row in rows:
    try:
        chemical = Chemical.objects.get(pk=row[1])
        plant = Plant.objects.get(pk=row[2])
        xref = XRef(xref_id=row[0], chemical_id=chemical, plant_id=plant, referenceCleanedDoi=row[3], referenceCleanedTitle=row[4], referenceCleanedPmcid=row[5], referenceCleanedPmid=row[6])
        xref.save()
    except Chemical.DoesNotExist:
        print(f'Chemical with id {row[1]} does not exist.')
    except Plant.DoesNotExist:
        print(f'Plant with id {row[2]} does not exist.')

db.close()

print("Script completed.")
