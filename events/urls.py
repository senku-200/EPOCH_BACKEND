from django.urls import path,include
from .views import register_participant,EventViewSet,InchargeViewSet,registerViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register',registerViewSet)
router.register(r'events',EventViewSet)
router.register(r'incharges',InchargeViewSet)
urlpatterns = [
    path('register/', register_participant, name='register_participant'),
    path('api/',include(router.urls))
]