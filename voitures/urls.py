from rest_framework.routers import DefaultRouter

from .views import VoitureViewSet

router=DefaultRouter()
router.register(r'voitures',VoitureViewSet,basename='voiture')
urlpatterns=router.urls