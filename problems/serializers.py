from rest_framework import serializers
from .models import Problem, Source

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('id', 'name', 'source', 'year')
