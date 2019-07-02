from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProblemSerializer
from django.http import JsonResponse
import dialogflow_v2 as dialogflow

from .models import Problem

from random import choices

class ProblemView(viewsets.ModelViewSet):
    serializer_class = ProblemSerializer
    queryset = Problem.objects.all()


def webhook(request):
    # Parse source list
    sources = request.POST.get()
    # Parse date
    start_date = 0
    end_date = 100000

    problem = choices(Problem.objects.filter(source__abbreviation__in=sources).filter(year__range=(start_date, end_date)))

    return JsonResponse(
        {
        }
    )
