from django.db import models

# Create your models here.

db_choices = (('Postgres','Postgres'), ('Gateway','Gateway'), ('Mongo','Mongo'))
category_choices = (('Accounts', 'Accounts'), ('Rolodex', 'Rolodex'))


class TotalStats(models.Model):
    id = models.AutoField(primary_key=True)
    database = models.CharField(max_length=15, null=False, choices=db_choices)
    category = models.CharField(max_length=15, null=False, choices=category_choices)
    name_of_table = models.CharField(max_length=255, null=False, blank=False)
    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)
    create_count = models.IntegerField(null=True)
    update_count = models.IntegerField(null=True)