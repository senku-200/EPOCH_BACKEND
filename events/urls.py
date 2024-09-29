from django.urls import path,include
from .views import register_participant,EventViewSet,InchargeViewSet,registerViewSet,CategoryViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'register',registerViewSet)
router.register(r'events',EventViewSet)
router.register(r'incharge',InchargeViewSet)
router.register(r'categories',CategoryViewSet)
urlpatterns = [
    path('register/', register_participant, name='register_participant'),
    path('api/',include(router.urls))
]