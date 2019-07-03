from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ProblemSerializer, SourceSerializer
import dialogflow_v2 as dialogflow

from .models import Problem, Source

from json import loads
from random import choices


class ProblemView(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()


def webhook(request):
    data = loads(request.body.decode('ascii'))
    sources = data['queryResult']['parameters']['source']
    start_date = int(data['queryResult']['parameters']['date-period']['startDate'][:4])
    end_date = int(data['queryResult']['parameters']['date-period']['endDate'][:4])

    problem = choices(Problem.objects.filter(
        source__abbreviation__in=sources, from_year__range=[start_date, end_date]))

    return JsonResponse(
        {
            'speech': 'Here is your problem',
            'displayText': f'{problem[0]}: {problem[0].url}',
            'source': 'cloudServiceMonitor',
        }
    )
