# Generated by Django 2.2.7 on 2020-09-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0007_auto_20200829_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='calcul_temps_TP_left',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_TP', models.IntegerField()),
                ('id_usr', models.IntegerField()),
                ('time_init', models.DateTimeField()),
                ('time_out', models.DateTimeField()),
                ('time_TP', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='1994-03-16'),
        ),
    ]
