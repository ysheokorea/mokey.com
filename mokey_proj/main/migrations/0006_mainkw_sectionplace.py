# Generated by Django 4.0 on 2022-01-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_mainkw_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainkw',
            name='sectionPlace',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
