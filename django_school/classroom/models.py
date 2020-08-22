from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    date_of_birth = models.DateField(default='11/11/2111')
    EQUIRED_FIELDS = ['date_of_birth']


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Quiz(models.Model):
    #enabled = models.BooleanField(verbose_name=_('enabled'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255 , default='Titre' , verbose_name= 'Titre TP',)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes', verbose_name= 'les filières',)

    type_tp_posible = (
        ('redressement et filtrage ', 'redressement et filtrage '),
        ('filtrage RC', 'filtrage RC'),
    )
    type_tp = models.CharField(max_length=500 ,choices=type_tp_posible , verbose_name= 'Type de circuit électrique')
    description = models.TextField( max_length=500 , verbose_name= 'Description de TP ')
    module = models.CharField(max_length=255, default='Matière' , verbose_name= 'Matière' )






    def __str__(self):
        labels = {
            "subject": "Embed"
        }
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)
    description = models.TextField( max_length=500 ,  verbose_name= 'Description de TP ')
    fiche_tp = models.FileField(upload_to='uploads_tp/' , verbose_name= 'Compte-rendu')


    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Subject, related_name='interested_students' )
    nome_student = models.CharField( max_length=255)

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        note = 10
        return questions


    def __str__(self):
        return self.user.username


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    compte_rendu = models.FileField(upload_to='uploads_tp/')
    correction_TP_ensegn  = models.FileField(upload_to='uploads_tp/')






class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    compte_rendu = models.FileField(upload_to='uploads_tp/')


class correction_TP(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True, blank=True, related_name='taken_quizzes')
    id_tp = models.IntegerField()
    nome_student = models.CharField(max_length=255, default='module')
    compte_rendu = models.FileField(upload_to='uploads_tp/')
    module = models.CharField(max_length=255, default='module')
    note = models.FloatField(default=0)
    id_user = models.IntegerField()

class evaluation_module(models.Model):
    id_user = models.IntegerField(default=0)
    note = models.FloatField(default=0)
    id_tp = models.IntegerField(default=0)







