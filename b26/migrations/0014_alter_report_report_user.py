# Generated by Django 4.2.11 on 2024-04-17 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('b26', '0013_report_upvoters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='b26.userprofile'),
        ),
    ]
