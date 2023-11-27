from django.shortcuts import render
from django.db import models

#Define Models
class Chemical(models.Model):
    chemical_id = models.IntegerField(primary_key=True)
    inchi_value = models.CharField(max_length=10000, null=True)
    pubchem_cid = models.CharField(max_length=1000, null=True)
    chembl_id = models.CharField(max_length=50, null=True)

class Plant(models.Model):

    class Meta:
        ordering = ['plant_id']

    plant_id = models.IntegerField(primary_key=True)
    taxonomy = models.CharField(max_length=5000, null=True)
    ncbi_species_id = models.CharField(max_length=1000, null=True)
    ncbi_subspecies_id = models.CharField(max_length=1000, null=True)

class XRef(models.Model):
    xref_id = models.IntegerField(primary_key=True)
    chemical_id = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='xrefs')
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='xrefs')
    referenceCleanedDoi = models.CharField(max_length=5000, null=True)
    referenceCleanedTitle = models.CharField(max_length=5000, null=True)
    referenceCleanedPmcid = models.CharField(max_length=1000, null=True)
    referenceCleanedPmid = models.CharField(max_length=1000, null=True)

class Drug(models.Model):

    class Meta:
        db_table = 'Drugs'
        
    drug_pair_id = models.IntegerField(primary_key=True)
    chemical_id = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='drugs', db_column='chemical_id')
    drug_chembl_id = models.CharField(max_length=200, null=True)
    tanimoto_similarity = models.FloatField(null=True)
    target_chembl_id = models.CharField(max_length=200, null=True)
    target_gene_id = models.CharField(max_length=100, null=True)


class Target(models.Model):
    target_gene_id = models.CharField(max_length=255, primary_key=True)
    target_synonyms = models.TextField(null=True)
    target_description = models.TextField(null=True)
    target_other_designations = models.TextField(null=True)
    target_ncbi_id = models.CharField(max_length=100, null=True)
    target_entrez_url = models.URLField(null=True)
    target_ensembl_id = models.CharField(max_length=100, null=True)
    target_ensembl_url = models.URLField(null=True)
    target_chembl_id = models.CharField(max_length=100, null=True)
    target_chembl_url = models.URLField(null=True)
    target_uniprot_id = models.CharField(max_length=100, null=True)
    target_cbioportal_url = models.URLField(null=True)
    target_ncigenomics_url = models.URLField(null=True)
    target_ncitargetdiscovery_url = models.URLField(null=True)
    target_cosmic_url = models.URLField(null=True)
    target_cancergeneticsweb_url = models.URLField(null=True)
    target_depmap_url = models.URLField(null=True)
    target_cansar_url = models.URLField(null=True)
