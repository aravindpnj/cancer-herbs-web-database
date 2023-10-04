from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Plant, Chemical, XRef, Drug
from django.core.paginator import EmptyPage, PageNotAnInteger


class HomePageView(ListView):
    model = Plant
    template_name = 'herbs/home.html'
    context_object_name = 'plants'
    ordering = ['plant_id']

    paginate_by = 30  # <--- specify the number of items per page

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if '=' in query:
                parts = query.split('=', 1)  # split only once
                identifier = parts[0].strip()
                value = parts[1].strip()
                if identifier == 'ncbi_species_id':
                    return Plant.objects.filter(ncbi_species_id__icontains=value)
                elif identifier == 'ncbi_subspecies_id':
                    return Plant.objects.filter(ncbi_subspecies_id__icontains=value)
                elif identifier == 'inchi_value':
                    return Plant.objects.filter(xrefs__chemical_id__inchi_value__icontains=value).distinct()
                elif identifier == 'pubchem_cid':
                    return Plant.objects.filter(xrefs__chemical_id__pubchem_cid__icontains=value).distinct()
                elif identifier == 'taxonomy':
                    return Plant.objects.filter(taxonomy__icontains=value)
            else:
                return Plant.objects.filter(
                    Q(ncbi_species_id__icontains=query) |
                    Q(ncbi_subspecies_id__icontains=query) |
                    Q(taxonomy__icontains=query) |
                    Q(xrefs__chemical_id__inchi_value__icontains=query) |
                    Q(xrefs__chemical_id__pubchem_cid__icontains=query)
                ).distinct()
        return Plant.objects.all().order_by('plant_id')

# def get_queryset(self):
#     query = self.request.GET.get('q')
#     search_type = self.request.GET.get('search_type', 'plant')  # default to 'plant' if not provided

#     print(f"Search Type: {search_type}")  # Debug print
#     print(f"Query: {query}")  # Debug print

#     if search_type == 'plant':
#         return Plant.objects.filter(
#             Q(taxonomy__icontains=query) |
#             Q(ncbi_species_id__icontains=query) |
#             Q(ncbi_subspecies_id__icontains=query)
#         )

#     elif search_type == 'chemical':
#         return Chemical.objects.filter(
#             Q(inchi_value__icontains=query) |
#             Q(pubchem_cid__icontains=query) |
#             Q(chembl_id__icontains=query)
#         )

#     plant_ids = XRef.objects.filter(chemical_id__in=matching_chemicals).values_list('plant_id', flat=True)
#     return Plant.objects.filter(plant_id__in=plant_ids)

#     # Default to showing all plants if no match
#     return Plant.objects.all()


class PlantDetailView(DetailView):
    model = Plant
    template_name = 'herbs/report.html'
    context_object_name = 'plant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plant = self.get_object()

        # Fetch related chemicals for the plant
        xrefs = XRef.objects.filter(plant_id=plant).select_related('chemical_id')

        # For each xref (which represents a chemical), fetch the count of associated drugs
        for xref in xrefs:
            xref.similar_drug_count = Drug.objects.filter(chemical_id=xref.chemical_id.chemical_id).count()

        # Sort the xrefs based on the similar_drug_count in descending order
        xrefs_sorted = sorted(xrefs, key=lambda x: x.similar_drug_count, reverse=True)

        # Build a list of unique chemicals and xrefs preserving the order
        seen_chemicals = set()
        unique_chemicals = []
        unique_xrefs = []
        for xref in xrefs_sorted:
            if xref.chemical_id not in seen_chemicals:
                seen_chemicals.add(xref.chemical_id)
                unique_chemicals.append(xref.chemical_id)
                unique_xrefs.append(xref)

        context['chemicals'] = unique_chemicals
        context['xrefs'] = unique_xrefs
        return context





class ChemicalDetailView(DetailView):
    model = Chemical
    template_name = 'herbs/chemical_detail.html'
    context_object_name = 'chemical'
    pk_url_kwarg = 'chemical_id'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chemical_id = self.get_object()

        # Fetch the plants this chemical is found in
        xrefs = XRef.objects.filter(chemical_id=chemical_id).select_related('plant_id')
        plants = list(set([xref.plant_id for xref in xrefs]))  # Using set to ensure distinct plants

        # Fetch similar drugs
        similar_drugs = Drug.objects.filter(chemical_id=chemical_id).order_by('-tanimoto_similarity')

        context['plants'] = plants
        context['similar_drugs'] = similar_drugs

        return context
