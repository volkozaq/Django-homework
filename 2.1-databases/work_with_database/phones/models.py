from django.db import models



class Phone(models.Model):
    name = models.TextField(max_length=100)
    price = models.IntegerField()
    image = models.TextField(max_length=100)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField( max_length=100, null=True)
