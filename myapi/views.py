from rest_framework import viewsets

from .serializers import HeroSerializer
from .models import Hero

from connectionWithDockerModel.main import xss_proccesor, predict_sqli_attack


class HeroViewSet(viewsets.ModelViewSet):
    queryset = Hero.objects.all().order_by('name')
    serializer_class = HeroSerializer