# Generated by Django 4.0 on 2022-01-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_rename_pubamountmonthmomentumkin_mainkw_pubamounttotalmomentumkin'),
    ]

    operations = [
        migrations.AddField(
            model_name='livekw',
            name='keywordNews',
            field=models.JSONField(blank=True, null=True),
        ),
    ]