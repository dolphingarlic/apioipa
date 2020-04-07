from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from problems import views

router = routers.DefaultRouter()
router.register(r'problems', views.ProblemView, 'problem')
router.register(r'sources', views.SourceView, 'source')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('webhook/', csrf_exempt(views.google_assistant_webhook), name='webhook'),
    path('random-problem/', csrf_exempt(views.random_problem), name='random-problem')
]
