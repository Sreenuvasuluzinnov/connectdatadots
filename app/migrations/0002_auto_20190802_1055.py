# Generated by Django 2.2.1 on 2019-08-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalstats',
            name='date_created',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='totalstats',
            name='date_updated',
            field=models.DateField(),
        ),
    ]
