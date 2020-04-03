from django.db import models


class SourceManager(models.Manager):
    def get_by_natural_key(self, abbreviation):
        return self.get(abbreviation=abbreviation)


class Source(models.Model):
    abbreviation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    objects = SourceManager()

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    url = models.URLField()
    from_year = models.IntegerField()
    image = models.URLField(null=True)

    def __str__(self):
        return f'{self.source.abbreviation} {self.from_year} - {self.name}'
