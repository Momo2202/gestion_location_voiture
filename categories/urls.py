from rest_framework.routers import DefaultRouter

from .views import CategorieViewSet

router=DefaultRouter()
round.register(r'categories',CategorieViewSet,basename='categorie')

urlpatterns = [
    router.urls
]
