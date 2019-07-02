from django.contrib import admin
from .models import Problem, Source


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'source', 'url', 'from_year')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Source)
