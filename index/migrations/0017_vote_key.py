# Generated by Django 2.2.10 on 2021-07-29 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0016_voter_activated'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='Key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]