from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .views import BreedViewSet, DogViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('breeds', BreedViewSet, basename='breeds')
router.register('dogs', DogViewSet, basename='dogs')


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
