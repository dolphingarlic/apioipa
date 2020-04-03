from json import loads
from random import choices

from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters

from .serializers import ProblemSerializer, SourceSerializer
from .models import Problem, Source


class ProblemView(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', '=source__abbreviation', '=from_year']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SourceView(viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=abbreviation']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def google_assistant_webhook(request):
    """
    Webhook for a Google Assistant action
    Returns a JSON payload
    """

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
                        'imageUri': problem.image,
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
                                        'url': problem.image,
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
