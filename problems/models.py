"""
Models for APIOIPA
"""

from django.db import models

class SourceManager(models.Manager):
    """
    Manager for a problem source
    """

    def get_by_natural_key(self, abbreviation):
        """
        Allows lookups by abbreviation
        """
        return self.get(abbreviation=abbreviation)


class Source(models.Model):
    """
    Class that represents a problem source
    e.g. BOI (Baltic Olympiad in Informatics)
    """

    abbreviation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    objects = SourceManager()

    def __str__(self):
        return self.name


class Problem(models.Model):
    """
    Class that represents a problem
    e.g. BOI 2019 - Nautilus
    """

    name = models.CharField(max_length=100)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)
    url = models.URLField()
    from_year = models.IntegerField()
    image = models.URLField(null=True)

    def __str__(self):
        return f'{self.source.abbreviation} {self.from_year} - {self.name}'

    class Meta:
        """
        Defines the ordering of problems
        """
        ordering = ('source', 'from_year',)
