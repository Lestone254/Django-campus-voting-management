# Generated by Django 2.2.10 on 2021-07-21 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20210720_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contestant',
            name='Type',
        ),
        migrations.AddField(
            model_name='election',
            name='Type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]