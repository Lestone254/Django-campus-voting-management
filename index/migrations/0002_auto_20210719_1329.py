# Generated by Django 2.2.10 on 2021-07-19 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='Election',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='index.Election'),
        ),
    ]
