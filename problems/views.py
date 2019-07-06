from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
import dialogflow_v2 as dialogflow

from .serializers import ProblemSerializer, SourceSerializer
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
    start_date = data['queryResult']['parameters']['start_date']
    end_date = data['queryResult']['parameters']['end_date']

    if start_date == -1:
        end_date = 9999
    elif end_date == -1:
        end_date = start_date

    if sources == ['any']:
        problem = choices(Problem.objects.filter(
            from_year__range=[start_date, end_date]))[0]
    else:
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
                        'imageUri': 'https://media.istockphoto.com/photos/binary-code-picture-id122204403?k=6&m=122204403&s=612x612&w=0&h=3_AdADaBrOZFIeAYhBA-u0-C6ZSrpMyD1FEX3uMdkC0=',
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
