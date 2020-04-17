'''
Serializers for APIOIPA models
'''

from rest_framework import serializers
from .models import Problem, Source


class SourceSerializer(serializers.ModelSerializer):
    '''
    Class that serializes a problem source
    '''

    class Meta:
        model = Source
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    '''
    Class that serializes a problem
    '''

    source = SourceSerializer(read_only=True)

    class Meta:
        model = Problem
        fields = '__all__'
