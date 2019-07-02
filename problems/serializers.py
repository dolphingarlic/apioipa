from rest_framework import serializers
from .models import Problem, Source

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('name', 'source', 'url', 'from_year')


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('abbreviation', 'name')
