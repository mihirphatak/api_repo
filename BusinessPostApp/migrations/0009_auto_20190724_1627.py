# Generated by Django 2.2.2 on 2019-07-24 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPostApp', '0008_auto_20190724_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspost',
            name='business_type',
            field=models.CharField(max_length=20),
        ),
    ]