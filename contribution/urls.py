from django.urls import path
from .views import (
    DocumentCategoryCreateView, 
    DocumentCategoryUpdateView,
    DocumentCategoryDeleteView
)

urlpatterns = [
    path('document/category/create/', DocumentCategoryCreateView.as_view(), name='document_category_create'),
    path('document/category/<slug>/update/', DocumentCategoryUpdateView.as_view(), name='document_category_update'),
    path('document/category/<slug>/delete/', DocumentCategoryDeleteView.as_view(), name='document_category_delete'),
]
