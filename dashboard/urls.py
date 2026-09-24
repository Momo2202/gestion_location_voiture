from django.urls import path

from .views import (
    LocationsRecentesView,
    RevenusParMoisView,
    StatsGlobalesView,
    TauxOccupationView,
    TopClientsView,
    TopVoituresView,
)


urlpatterns = [
    path('dashboard/stats/', StatsGlobalesView.as_view(), name='dashboard-stats'),
    path('dashboard/revenus/', RevenusParMoisView.as_view(), name='dashboard-revenus'),
    path('dashboard/occupation/', TauxOccupationView.as_view(), name='dashboard-occupation'),
    path('dashboard/top-voitures/', TopVoituresView.as_view(), name='dashboard-top-voitures'),
    path('dashboard/top-clients/', TopClientsView.as_view(), name='dashboard-top-clients'),
    path('dashboard/locations-recentes/', LocationsRecentesView.as_view(), name='dashboard-locations-recentes'),
]