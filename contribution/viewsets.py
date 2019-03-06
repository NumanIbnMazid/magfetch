from rest_framework import viewsets
from .models import Contribution
from .serializers import ContributionSerializer


class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
