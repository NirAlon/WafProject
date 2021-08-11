from rest_framework import serializers

from .models import Hero, Waf

class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('name', 'alias')

class WafSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Waf
        fields = ('sql_injection','xss_attack')