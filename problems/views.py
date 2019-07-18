from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
import dialogflow_v2 as dialogflow

from .serializers import ProblemSerializer, SourceSerializer
from .models import Problem, Source

from json import loads
from random import choices


urls = {
    'APIO': 'https://i.imgur.com/Nn9yRKA.jpg',
    'BOI': 'https://i.imgur.com/H1b0YZt.jpg',
    'CEOI': 'https://i.imgur.com/npq19Ar.jpg',
    'IOI': 'https://i.imgur.com/PzGjiM8.jpg',
    'JOI': 'https://i.imgur.com/rSlkMO4.jpg',
    'POI': 'https://i.imgur.com/rb2CbPU.jpg',
    'SACO': 'https://i.imgur.com/RZajrYJ.jpg',
}


class ProblemView(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()


def webhook(request):
    data = loads(request.body.decode('ascii'))
    sources = data['queryResult']['parameters']['source']
    start_date = int(data['queryResult']['parameters']['start_date'])
    end_date = int(data['queryResult']['parameters']['end_date'])

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
            'responseId': data['responseId'],
            'fulfillmentMessages': [
                {
                    'card': {
                        'title': problem.name,
                        'subtitle': f'{problem.source.abbreviation} {problem.from_year}',
                        'imageUri': urls[problem.source.abbreviation],
                        'buttons': [
                            {
                                'text': 'Open in your browser',
                                'postback': problem.url
                            }
                        ]
                    }
                }
            ],
            'payload': {
                'google': {
                    'expectUserResponse': True,
                    'richResponse': {
                        'items': [
                            {
                                'simpleResponse': {
                                    'textToSpeech': f'Task {problem.name} from the {problem.from_year} {problem.source.name}'
                                }
                            },
                            {
                                'basicCard': {
                                    'title': problem.name,
                                    'subtitle': f'{problem.source.abbreviation} {problem.from_year}',
                                    'formattedText': f'Task {problem.name} from the {problem.from_year} {problem.source.name}',
                                    'image': {
                                        'url': urls[problem.source.abbreviation],
                                        'accessibilityText': f'{problem.source.abbreviation} Logo',
                                    },
                                    'buttons': [
                                        {
                                            'title': 'Open in your browser',
                                            'openUrlAction': {
                                                'url': problem.url
                                            }
                                        }
                                    ],
                                    'imageDisplayOptions': 'CROPPED'
                                }
                            }
                        ]
                    }
                }
            }
        },
        safe=False
    )
