from django.shortcuts import render
from django.http import JsonResponse
import dialogflow_v2 as dialogflow
import json

from .models import Problem

from random import choices

def webhook(request):
    data = json.loads(request.body)
    # Parse source list
    sources = data['queryResult']['parameters']['source']
    # Parse date
    start_date = int(data['queryResult']['parameters']['dste-period']['startDate'][:4])
    end_date = int(data['queryResult']['parameters']['dste-period']['endDate'][:4])

    problem = choices(Problem.objects.filter(source__abbreviation__in=sources).filter(year__range=(start_date, end_date)))

    return JsonResponse(
        {
            'speech': 'Yeet',
            'displayText': problem.id,
            'source': 'cloudServiceMonitor',
        }
    )
