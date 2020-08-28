import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, correction_TP_Form
from ..models import Quiz, Student, TakenQuiz, User, Question, correction_TP
import os
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse, JsonResponse, HttpResponseRedirect
import requests as RG
from django.contrib.sessions.models import Session
import subprocess
import json
from pickle import dump, load, Unpickler
from datetime import datetime, timedelta

#
from requests import get
import pickle



class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_interests = student.interests.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    #print(correction_TP.objects.all())
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student


    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    # quiz == nome TP
    #print('fffffffff', quiz)

    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()
    print(request.user.pk)
    print('student.pk ==== ', student.pk)
    ####" get path fiche.bin ####
    your_media_root = settings.MEDIA_ROOT  # /root/Desktop/testdjangoschool/src/django_school/media

    path_bin = your_media_root + '/' + 'fiche.bin'

    f = open(path_bin, 'rb')
    m1 = load(f)
    #m1 = '0111111'
    f.close()
    print(m1)
    print(request.user.pk)

    if (m1[0] == '0'  or  m1[4] == str(request.user.pk)) or (datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') < datetime.now() ) and (m1[1] != str(request.user.pk)):
        #with open(path_bin, 'wb') as f:
            #dump((['0','ID_usr_block',  'time_in' ,'time_out' , 'ID_usr_current' ]), f)
        temps_TP =  Quiz.objects.get(pk = pk)
        print('temps_TP ===== ',temps_TP.Temps_TP)
        now = datetime.now()
        time_init = now.strftime("%b %d %Y %H:%M:%S")
        time_out_ = now +  timedelta(seconds = 60 * int(temps_TP.Temps_TP)  )
        time_out = time_out_.strftime("%b %d %Y %H:%M:%S")
        #print('time init ====' , time_init)
        #print('m1[3] time out fiche bin  ' , m1[3])
        #print(time_init < m1[3])
        #print(datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') -now ) #"%b %d %Y %H:%M:%S.%f"
        if not (time_init < m1[3]) :
            print('time oveeeeeeer')
        print(m1)
        if m1[4] != str(request.user.pk)  :
            f = open(path_bin, 'wb')
            dump((['1', 'ID_usr_block', str(now), str(time_out_), str(request.user.pk)]), f)
            print('done --------- ')
            f.close()
            #time_left = datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') - now
        if m1[4] == str(request.user.pk) :
            if  (datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') < now ) :
                print('not time_init < m1[3]')
                print(time_init  < m1[3])
                f = open(path_bin, 'wb')
                dump((['0', str(request.user.pk), '0',str(time_out_),'0']), f)
                f.close()
                messages.warning(request, 'time is over')
                return redirect('students:quiz_list')
        #Unpickler(f).load()
        print(time_init)
        print(time_out)
        now = datetime.now()
        #time_left =  datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') - now

        time_left =  datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') - now
        time_left_scnd = time_left.seconds

        print(time_left_scnd)
        if time_left_scnd > int(temps_TP.Temps_TP) * 60  :
            time_left_scnd =  60 * int(temps_TP.Temps_TP)

            #
        #f.close()






        if request.method == 'POST':
            #form = TakeQuizForm(question=question, data=request.POST)
            form = correction_TP_Form(request.POST , request.FILES)




            if form.is_valid() :
                f = open(path_bin, 'wb')
                dump((['0', '0', '0', str(time_out_), '0']), f)
                f.close()



                with transaction.atomic():
                    student_answer = form.save(commit=False)
                    #f = correction_TP.objects.get(user = request.user)
                    #f = 'hemidi benameur'
                    #print('fffff=', 'hemidi/ol')
                    #student_answer.student = student
                    #print('student.pk ====' ,student.pk )
                    student_answer.id_tp =  question.pk
                    student_answer.id_user =  student.pk

                    student_answer.save()
                    if student.get_unanswered_questions(quiz).exists() and False:
                        return redirect('students:take_quiz', pk)
                    else:
                        #correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()

                        h = correction_TP.objects.get(id_tp = question.pk , id_user = student.pk )
                        print('correction_TP.objects.get() ==== ',h.compte_rendu)
                        #f = correction_TP.objects.get(user=student.user)

                        score = 100.0
                        TakenQuiz.objects.create(student=student, quiz=quiz, score=score ,compte_rendu = h.compte_rendu  )


                        if score < 50.0:
                            messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                        else:
                            messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                        return redirect('students:quiz_list')
        else:
            form = correction_TP_Form()

        return render(request, 'classroom/students/take_quiz_form.html', {
            'quiz': quiz,
            'question': question,
            'form': form,
            'progress': progress ,
            'time_left' : time_left_scnd,
        })
    else:
        messages.warning(request, 'Please come back after')
        return redirect('students:quiz_list')



############ this add  mi
'''
class Compt_rendu(TemplateView ):
    print('compt rendu is si sis sisi')

    def get_context_data(self, request,**kwargs):
        print('compt rendu is si sis sisi')
        path = ' '
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
        '''

def pdf_view(request, id):
    all_postes_ = Question.objects.get(id=id)
    #print(all_postes_.fiche_tp)
    p = request.POST.get('variable')
    print(p)

    contax = {
        'all_post': all_postes_,

    }

    #return render(request, 'pdf_views.html', contax)
    #file_path = os.path.join(settings.MEDIA_ROOT, all_postes_.fiche_tp)
    your_media_root = settings.MEDIA_ROOT #/root/Desktop/testdjangoschool/src/django_school/media

    path_pdf =  your_media_root  + '/' + str(all_postes_.fiche_tp)

    #print(your_media_root)
    try:
        return FileResponse(open(path_pdf, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')


@login_required
@student_required
def get_vr(request, id , r):
    print(request.session.keys())
    session_key = request.session.session_key
    # date 2 heur
    #request.session.clear_expired()
    #request.session.clearsessions()
    print('jjjjjjj =========' ,  session_key.startswith("_"))
  
    print(' blocer after ==== ' ,     Session.objects.all().count())
    print(' llllllll ==== ' ,     request.session.exists(Session.objects.all()[0]) )
    #Session.objects.all().delete()
    #print('session_key ========' , session_key)
    #print('yes' , r)
    ip = get('https://api.ipify.org').text

    # if  switch 1 deux position utilise GPIO 5  place 29
    subprocess.call(['gpio', '-g', 'mode', '5', 'out'])
    subprocess.call(['gpio', '-g', 'write', '5', '1'])

    contax = {
        'urle': 'http://'+ip + ':5000/' ,

    }
    if Session.objects.all().count() >  1 :
        if str(session_key) == str(Session.objects.all()[0]) :

            print(' blocer after ==== ', Session.objects.all().count())
            #cartTP('000000') # initialisation
            request.session.set_expiry(50)
            return render(request, 'classroom/students/osilo.html' , contax)
        else :
            return render(request, '500.html')
    else :

        return render(request, 'classroom/students/osilo.html',contax)

'''
def cartTP(statuspin) :
    #print('statuspin  ===== ', STATUSPIN)
    switch1 = [statuspin[0] , '17' ]
    switch2 = [statuspin[1] , '27' ]
    switch3 = [statuspin[1] , '22' ]
    switch4 = [statuspin[1] , '10' ]
    switch5 = [statuspin[1] , '09' ]
    switch6 = [statuspin[1] , '11' ]
    switchall = [switch1 , switch2, switch3 , switch4 , switch5 , switch6]
    #switch7 = statuspin[6]
    for  switch in switchall :
        #subprocess.call(['gpio' , '-g' , 'mode' , switch[1] , 'out'])
        print(['gpio' , '-g' , 'mode' , switch[1] , 'out'])
        #subprocess.call(['gpio' , '-g' , 'wirite' , switch[1] , switch[0]])
        print(['gpio' , '-g' , 'write' , switch[1] , switch[0]])
'''


def test_redirect(request):
    url = request.get_full_path()
    #return HttpResponseRedirect("wwww.192.168.1.20.com")
    return  redirect('/')

############## coper
"""
@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })


"""


@login_required
@require_POST
@csrf_exempt
def like(request):
    if request.method == 'POST':
        switchs = {'switch_1' : '17' , 'switch_2' : '27','switch_3' : '22',
                   'switch_4' : '10' , 'switch_5' : '09' , 'switch_6' : '11' ,
                   'switch_7' : '0000' }
        data = request.body
        switch = str(data).split('&')[0].split('=')[1]
        status = str(data).split('&')[1].split('=')[1][:-1]
        if switch == 'switch_1' and status == 1 :
            subprocess.call(['gpio', '-g', 'mode', '5', 'out'])
            subprocess.call(['gpio', '-g', 'write', '5', '0'])
        if switch == 'switch_1' and status == 0:
            subprocess.call(['gpio', '-g', 'mode', '5', 'out'])
            subprocess.call(['gpio', '-g', 'write', '5', '1'])

        subprocess.call(['gpio' , '-g' , 'mode' , switchs[switch] , 'out'])
        #print(['gpio', '-g', 'mode', switchs[switch], 'out'])
        subprocess.call(['gpio' , '-g' , 'wirite' , switchs[switch] , status])
        #print(['gpio', '-g', 'write', switchs[switch] , status])


    ctx = {'likes_count': 'rt', 'message':'ffffff'}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')



@login_required
def pdf_corect(request):
    #print(all_postes_.fiche_tp)
    p = request.GET.get('date')
    #file_path = os.path.join(settings.MEDIA_ROOT, all_postes_.fiche_tp)
    your_media_root = settings.MEDIA_ROOT #/root/Desktop/testdjangoschool/src/django_school/media

    path_pdf =  your_media_root  + '/' + str(p)

    #print(your_media_root)
    try:
        return FileResponse(open(path_pdf, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')
