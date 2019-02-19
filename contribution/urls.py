from django.urls import path
from .views import (
    DocumentCategoryCreateView, 
    DocumentCategoryUpdateView,
    DocumentCategoryDeleteView,
    DocumentUploadView,
    ImageUploadView
)

urlpatterns = [
    path('document/category/create/', DocumentCategoryCreateView.as_view(), name='document_category_create'),
    path('document/category/<slug>/update/', DocumentCategoryUpdateView.as_view(), name='document_category_update'),
    path('document/category/<slug>/delete/', DocumentCategoryDeleteView.as_view(), name='document_category_delete'),
    path('document/upload/', DocumentUploadView.as_view(), name='document_upload'),
    path('image/upload/', ImageUploadView.as_view(), name='image_upload'),
]
