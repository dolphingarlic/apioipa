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
    start_date = int(data['queryResult']['parameters']
                     ['date-period']['startDate'][:4])
    end_date = int(data['queryResult']['parameters']
                   ['date-period']['endDate'][:4])

    problem = choices(Problem.objects.filter(
        source__abbreviation__in=sources, from_year__range=[start_date, end_date]))[0]

    return JsonResponse(
        {
            'fulfillmentText': str(problem),
            'fulfillmentMessages': [
                {
                    'card': {
                        'title': problem.name,
                        'subtitle': f'{problem.source.abbreviation} {problem.from_year}',
                        'imageUri': 'https://upload.wikimedia.org/wikipedia/commons/3/34/IOI_logo.png',
                        'buttons': [
                            {
                                'text': 'Open in your browser',
                                'postback': problem.url
                            }
                        ]
                    }
                }
            ],
        }
    )
