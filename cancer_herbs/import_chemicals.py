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


print("Starting script...")
# Connect to your MySQL database
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="8nanyangdrive", db="cancer_herbs_database")

cursor = db.cursor()

# Fetch data from the Chemicals table
print("Fetching data from Chemicals table...")
cursor.execute("SELECT * FROM Chemicals")
rows = cursor.fetchall()

# Create a list to hold the Chemical instances
chemicals = []

# Create a Chemicals instance for each row and add it to the list
print("Creating Chemical instances...")
for row in rows:
    chemical = Chemical(chemical_id=row[0], inchi_value=row[1], pubchem_cid=row[2], chembl_id=row[3])
    chemicals.append(chemical)

# Use bulk_create to save all Chemical instances to the Django database
print("Saving data to Django database...")
Chemical.objects.bulk_create(chemicals)

# Do the same for the Plants and XRef tables

db.close()
print("Script completed.")
