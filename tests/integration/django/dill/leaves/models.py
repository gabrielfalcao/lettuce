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


class Field(models.Model):
    name = models.CharField(max_length=100)


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    garden = models.ForeignKey(Garden)
    ripe_by = models.DateField()
    fields = models.ManyToManyField(Field)


class Bee(models.Model):
    name = models.CharField(max_length=100)
    pollinated_fruit = models.ManyToManyField(Fruit,
                                              related_name='pollinated_by')


class Goose(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "geese"


class Harvester(models.Model):
    make = models.CharField(max_length=100)
    rego = models.CharField(max_length=100)


class Panda(models.Model):
    """
    Not part of a garden, but still an important part of any good application
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
