# Generated by Django 3.2.4 on 2021-11-23 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('part1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='org_name',
        ),
    ]
