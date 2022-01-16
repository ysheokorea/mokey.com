# Generated by Django 4.0 on 2022-01-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_expandkeyword_expandkeyword_unique expand_keyword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainkw',
            name='pubAmountMonthMomentum',
        ),
        migrations.RemoveField(
            model_name='mainkw',
            name='pubAmountTotal',
        ),
        migrations.RemoveField(
            model_name='mainkw',
            name='pubAmountTotalMomentum',
        ),
        migrations.RemoveField(
            model_name='mainkw',
            name='pubAmountTotalMomentumKin',
        ),
        migrations.RemoveField(
            model_name='mainkw',
            name='searchMOBILEMomentum',
        ),
        migrations.RemoveField(
            model_name='mainkw',
            name='searchPCMomentum',
        ),
        migrations.AddField(
            model_name='mainkw',
            name='pubAmountTotalBlog',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mainkw',
            name='pubAmountTotalCafe',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]