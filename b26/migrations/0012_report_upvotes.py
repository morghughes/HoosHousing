# Generated by Django 4.2.10 on 2024-04-12 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b26', '0011_merge_20240412_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
