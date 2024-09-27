from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, NLPCommandView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('nlp-command/', NLPCommandView.as_view(), name='nlp-command'),
]
