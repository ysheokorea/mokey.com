# Generated by Django 4.0 on 2022-01-12 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_remove_mainkw_pubamountmonthmomentum_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keywordhistory1',
            old_name='pubAmountTotal',
            new_name='pubAmountTotalBlog',
        ),
    ]