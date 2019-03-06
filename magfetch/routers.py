from rest_framework import routers
from contribution.viewsets import ContributionViewSet


router = routers.DefaultRouter()


router.register(r'contribution', ContributionViewSet)
