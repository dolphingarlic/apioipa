from django.db import models


class Source(models.Model):
    abbreviation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    url = models.URLField(default='https://oj.uz/')
    from_year = models.IntegerField()

    def __str__(self):
        return f'{self.source.abbreviation} {self.from_year} - {self.name}'
