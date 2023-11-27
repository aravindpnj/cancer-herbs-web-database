from django.shortcuts import render, get_object_or_404, redirect
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


    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('search_type')
        search_field = self.request.GET.get('search_field')
        
        if search_type == 'Chemical' and search_field in ['inchi_value', 'pubchem_cid']:
            chemical = Chemical.objects.filter(**{search_field: query}).first()
            if chemical:
                return redirect('herbs:chemical_detail', chemical_id=chemical.chemical_id)
        
        return super().get(request, *args, **kwargs)



    def get_queryset(self):
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('search_type')
        search_field = self.request.GET.get('search_field')

        if search_type and search_field:
            if search_type == 'Plant':
                if search_field == 'ncbi_species_id':
                    return Plant.objects.filter(
                        Q(ncbi_species_id__icontains=query) | 
                        Q(ncbi_subspecies_id__icontains=query)
                    )
                elif search_field == 'taxonomy':
                    return Plant.objects.filter(taxonomy__icontains=query)
            
            # If the user selects an invalid combination, show no results
            return Plant.objects.none()

        # If we reach here, no search parameters were provided
        # Returning all plants as a default behavior
        return Plant.objects.all()






    

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        # Get the current page number from the paginator
        page = context['page_obj'].number

        # Calculate the start and end pages for the fixed range
        start_page = ((page - 1) // 10) * 10 + 1
        end_page = start_page + 9

        # Ensure end_page doesn't exceed the maximum number of pages
        end_page = min(end_page, context['paginator'].num_pages)
        
        # Create the range of page numbers
        context['page_range'] = range(start_page, end_page + 1)
        
        return context




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
