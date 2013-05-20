from django.db import models

class Garden(models.Model):
    name = models.CharField(max_length=100)
    area = models.IntegerField()
    raining = models.BooleanField()

    @property
    def howbig(self):
        if self.area < 50:
            return 'small'
        elif self.area < 150:
            return 'medium'
        else:
            return 'big'

class Fruit(models.Model):
    name = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden)
    ripe_by = models.DateField()

class Goose(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "geese"

class Harvester(models.Model):
    make = models.CharField(max_length=100)
    rego = models.CharField(max_length=100)
