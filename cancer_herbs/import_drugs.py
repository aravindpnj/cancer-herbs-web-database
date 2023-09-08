import MySQLdb
import os
import django

# Set the Django settings module environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cancer_herbs.settings")

# Initialize Django
django.setup()

# Now you can import your Django models
from herbs.models import Chemical, Drug

print("Starting script...")

# Connect to the MySQL database
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="8nanyangdrive", db="cancer_herbs_database")

# Create a cursor object to interact with the database
cursor = db.cursor()

# Fetch data from Drugs table
cursor.execute("SELECT * FROM Drugs;")
rows = cursor.fetchall()

print("Fetching data from Drugs table...")

print("Saving data...")

# Create a Drug instance for each row and save it to the Django database
for row in rows:
    try:
        chemical = Chemical.objects.get(pk=row[1])
        drug = Drug(drug_pair_id = row[0], chemical_id = chemical, drug_chembl_id=row[2], tanimoto_similarity=row[3], target_chembl_id=row[4], target_gene_id=row[5])
        drug.save()
    except Chemical.DoesNotExist:
        print(f'Chemical with id {row[0]} does not exist.')

db.close()

print("Script completed.")
