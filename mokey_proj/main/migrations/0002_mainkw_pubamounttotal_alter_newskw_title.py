# Generated by Django 4.0 on 2021-12-27 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainkw',
            name='pubAmountTotal',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newskw',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]