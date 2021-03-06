from django.urls import path
from .views import (
    ContributionCategoryCreateView,
    ContributionCategoryUpdateView,
    ContributionCategoryDeleteView,
    ContributionUploadView,
    ContributionListView,
    ContributionDetailView,
    SelectedContributionListView,
    mark_as_selected,
    mark_as_unselected,
    contribution_delete,
    comment_create,
    CommentListView
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
    path('delete/', contribution_delete, name='contribution_delete'),
    path('<slug>/detail/', ContributionDetailView.as_view(), name='contribution_detail'),
    path('list/', ContributionListView.as_view(), name='contribution_list'),
    path('selected/list/', SelectedContributionListView.as_view(), name='selected_contribution_list'),
    path('<slug>/mark/selected/', mark_as_selected, name='contribution_selected'),
    path('<slug>/mark/unselected/', mark_as_unselected, name='contribution_unselected'),
    #comment
    path('comment/<slug>/create/', comment_create, name='comment_create'),
    path('comment/<slug>/view/', CommentListView.as_view(), name='comment_view'),
]
