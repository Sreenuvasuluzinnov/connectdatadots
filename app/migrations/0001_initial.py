# Generated by Django 2.2.4 on 2019-08-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TotalStats',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('database', models.CharField(choices=[('Postgres', 'Postgres'), ('Gateway', 'Gateway'), ('Mongo', 'Mongo')], max_length=15)),
                ('category', models.CharField(choices=[('Accounts', 'Accounts'), ('Rolodex', 'Rolodex')], max_length=15)),
                ('name_of_table', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('create_count', models.IntegerField(null=True)),
                ('update_count', models.IntegerField(null=True)),
            ],
        ),
    ]