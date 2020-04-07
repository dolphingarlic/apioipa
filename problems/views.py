from json import loads
from random import choice

from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(['GET'])
def random_problem(request):
    problem = choice(Problem.objects.all())
    serializer = ProblemSerializer(problem)
    return Response(serializer.data)


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
        problem = choice(Problem.objects.filter(
            from_year__range=[start_date, end_date]))
    else:
        problem = choice(Problem.objects.filter(
            source__abbreviation__in=sources, from_year__range=[start_date, end_date]))

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
