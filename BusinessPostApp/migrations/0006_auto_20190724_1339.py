# Generated by Django 2.2.2 on 2019-07-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPostApp', '0005_auto_20190724_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspost',
            name='business_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'business'), (2, 'service'), (3, 'classes')]),
        ),
    ]
