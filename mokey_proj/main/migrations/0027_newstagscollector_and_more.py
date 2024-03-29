# Generated by Django 4.0 on 2022-01-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_remove_livekw_unique livekw_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsTagsCollector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags_title', models.CharField(blank=True, max_length=300, null=True)),
                ('tags_count', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'newstagscollector',
            },
        ),
        migrations.AddConstraint(
            model_name='newstagscollector',
            constraint=models.UniqueConstraint(fields=('tags_title', 'created_on'), name='unique newstagscollector'),
        ),
    ]
