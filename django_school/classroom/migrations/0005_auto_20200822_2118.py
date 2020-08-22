# Generated by Django 2.2.7 on 2020-08-22 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_evaluation_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='takenquiz',
            name='correction_TP_ensegn',
            field=models.FileField(default=0, upload_to='uploads_tp/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Description de TP '),
        ),
        migrations.AlterField(
            model_name='question',
            name='fiche_tp',
            field=models.FileField(upload_to='uploads_tp/', verbose_name='Compte-rendu'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Description de TP '),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='module',
            field=models.CharField(default='Matière', max_length=255, verbose_name='Matière'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(default='Titre', max_length=255, verbose_name='Titre TP'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='classroom.Subject', verbose_name='les filières'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='type_tp',
            field=models.CharField(choices=[('redressement et filtrage ', 'redressement et filtrage '), ('filtrage RC', 'filtrage RC')], max_length=500, verbose_name='Type de circuit électrique'),
        ),
    ]
