# Generated by Django 4.0 on 2022-01-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mainkw_pubamountmonthmomentum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainkw',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
