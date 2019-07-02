from django.contrib import admin
from .models import Problem, Source


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'source', 'year')


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Source)
