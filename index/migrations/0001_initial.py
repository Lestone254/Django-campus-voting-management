# Generated by Django 2.2.10 on 2021-07-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=60)),
                ('Type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RegNo', models.CharField(max_length=50)),
                ('FirstName', models.CharField(max_length=60)),
                ('LastName', models.CharField(max_length=50)),
                ('School', models.CharField(max_length=50)),
                ('Department', models.CharField(max_length=70)),
                ('Email', models.CharField(max_length=60)),
                ('Number', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=60)),
                ('Votes', models.IntegerField()),
                ('Individual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Voter')),
                ('Post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Post')),
            ],
        ),
    ]
