"""
Serializers for APIOIPA models
"""

from rest_framework import serializers
from .models import Problem, Source


class ProblemSerializer(serializers.ModelSerializer):
    """
    Class that serializes a problem
    """

    class Meta:
        model = Problem
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    """
    Class that serializes a problem source
    """

    class Meta:
        model = Source
        fields = '__all__'
