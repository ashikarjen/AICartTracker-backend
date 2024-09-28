from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, NaturalLanguageInputView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('nlp-input/', NaturalLanguageInputView.as_view(), name='nlp-input'),
]
