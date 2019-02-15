from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100, null=True, default='')
    ticker = models.CharField(max_length=10, null=True, default='')