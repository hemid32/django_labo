# Generated by Django 2.2.7 on 2020-06-23 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_create_initial_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='nome_student',
            field=models.CharField(default='hemidi benameur', max_length=255, verbose_name='Answer'),
            preserve_default=False,
        ),
    ]
