from django.urls import path,include
from .views import register_participant,EventViewSet,InchargeViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'events',EventViewSet)
router.register(r'incharges',InchargeViewSet)
urlpatterns = [
    path('register/', register_participant, name='register_participant'),
    path('api/',include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)