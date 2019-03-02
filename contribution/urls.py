from django.urls import path
from .views import (
    ContributionCategoryCreateView,
    ContributionCategoryUpdateView,
    ContributionCategoryDeleteView,
    ContributionUploadView,
)

urlpatterns = [
    # Contribution Category
    path('category/create/', ContributionCategoryCreateView.as_view(),
         name='category_create'),
    path('category/<slug>/update/', ContributionCategoryUpdateView.as_view(),
         name='category_update'),
    path('category/<slug>/delete/', ContributionCategoryDeleteView.as_view(),
         name='category_delete'),
    # Contribution
    path('upload/', ContributionUploadView.as_view(), name='upload'),
]
