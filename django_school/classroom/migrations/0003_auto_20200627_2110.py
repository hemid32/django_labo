# Generated by Django 2.2.7 on 2020-06-27 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_create_initial_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='fiche_tp',
            field=models.FileField(default=0, upload_to='uploads_tp/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.TextField(default=0, max_length=500, verbose_name='description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='module',
            field=models.CharField(default='module', max_length=255),
        ),
        migrations.AddField(
            model_name='quiz',
            name='type_tp',
            field=models.CharField(choices=[('RC', 'RC'), ('R', 'R'), ('RL', 'RL')], default=0, max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='nome_student',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentanswer',
            name='compte_rendu',
            field=models.FileField(default=0, upload_to='uploads_tp/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='takenquiz',
            name='compte_rendu',
            field=models.FileField(default=0, upload_to='uploads_tp/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(max_length=500, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='nome TP', max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default='11/11/2111'),
        ),
        migrations.CreateModel(
            name='correction_TP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tp', models.IntegerField()),
                ('nome_student', models.CharField(default='module', max_length=255)),
                ('compte_rendu', models.FileField(upload_to='uploads_tp/')),
                ('module', models.CharField(default='module', max_length=255)),
                ('note', models.FloatField(default=0)),
                ('id_user', models.IntegerField()),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taken_quizzes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]