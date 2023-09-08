# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.HomePageView, name='home'),
#     path('results/', views.ResultsPageView, name='results'),
#     path('detail/<int:pk>/', views.DetailPageView, name='detail'),
# ]
from django.urls import path
from .views import HomePageView, PlantDetailView, ChemicalDetailView
app_name = 'herbs'

urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),
    path('report/<int:pk>/', PlantDetailView.as_view(), name='report'),
    path('chemical/<int:chemical_id>/', ChemicalDetailView.as_view(), name='chemical_detail')
]
