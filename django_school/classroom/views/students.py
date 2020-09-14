import os

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from ..decorators import student_required
from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm, correction_TP_Form
from ..models import Quiz, Student, TakenQuiz, User, Question, correction_TP, Planning_TP, calcul_temps_TP_left
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
import pytz



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
        # Planning
        #print('4444444444 ======= ',len(queryset))
        #print(queryset)

        for id  in queryset.values() :
            id_tp = id['id']
            #print(id)
            #print(id['Temps_TP'])

            #print(id_tp)
            try:
                pl = Planning_TP.objects.get(id_TP = id_tp , id_usr =  self.request.user.pk )


            except:
                pl = False

            if pl == False :
                # get time in finale
                if len(Planning_TP.objects.filter(id_TP = id_tp).values()) != 0 :
                    time_fn_final =  Planning_TP.objects.filter(id_TP = id_tp).values()
                    print(id_tp)
                    temps_tp  =  Planning_TP.objects.filter(id_TP = id_tp).values()[len(time_fn_final)-1]['time_TP']
                    time_in =  Planning_TP.objects.filter(id_TP = id_tp).values()[len(time_fn_final)-1]['time_fn']
                    time_fn =  Planning_TP.objects.filter(id_TP = id_tp).values()[len(time_fn_final)-1]['time_fn'] + + timedelta(minutes=60 * 12)
                    #print(time_in  , time_fn)
                    Planning_TP.objects.create(id_usr = self.request.user.pk , id_TP = id_tp , time_in = time_in , time_fn = time_fn , time_TP = temps_tp)
                else :
                    time_in = datetime.now()
                    time_fn = time_in + timedelta(minutes=60 * 12)
                    temps_tp = id['Temps_TP']
                    id_usr = self.request.user.pk
                    id_tp = id_tp
                    # print(time_in, time_fn, id_usr , id_tp , temps_tp )
                    Planning_TP.objects.create(id_usr=id_usr, id_TP=id_tp, time_in=time_in, time_fn=time_fn,
                                               time_TP=temps_tp)
                    # Planning_TP.save()
            else :
                #print('yesssssssss')
                pass

        # Planning
        return queryset
    # contex pour Planning
    def get_context_data(self, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)  # get the default context data
        context['time'] = Planning_TP.objects.filter(id_usr=self.request.user.pk ).values()  # add extra field to the context
        return context


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

    #with open(path_bin, 'wb') as f:
        #dump((['0','ID_usr_block',  'time_in' ,'time_out' , 'ID_usr_current' ]), f)
    temps_TP =  Quiz.objects.get(pk = pk)
    #now = datetime.now()
    #time_init = now.strftime("%b %d %Y %H:%M:%S")
    #time_out = time_out_.strftime("%b %d %Y %H:%M:%S")
    #print('time init ====' , time_init)
    #print('m1[3] time out fiche bin  ' , m1[3])
    #print(time_init < m1[3])
    #print(datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') -now ) #"%b %d %Y %H:%M:%S.%f"

    #Unpickler(f).load()

    #time_left =  datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') - now

    #time_left =  datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f') - now

    ## Planning
    #datetime.strptime(m1[3], '%Y-%m-%d %H:%M:%S.%f')

    Planning  =  Planning_TP.objects.get(id_usr = request.user.pk , id_TP = pk)
    print(Planning.time_in.strftime("%b %d %Y %H:%M:%S"))

    if datetime.strptime(Planning.time_in.strftime("%Y-%m-%d %H:%M:%S.%f"), '%Y-%m-%d %H:%M:%S.%f') < datetime.now() and datetime.strptime(Planning.time_fn.strftime("%Y-%m-%d %H:%M:%S.%f"), '%Y-%m-%d %H:%M:%S.%f') > datetime.now() :







        # pout activer timing  ( tomporery)
        #now = datetime.now()
        try:
            calcul_temps_TP = calcul_temps_TP_left.objects.get(id_usr=request.user.pk, id_TP=pk)
            target = True
            #print('target = True : ', calcul_temps_TP)
        except :
            target = False
            #print('target = False : ')

        if target == True :
            #time_now = now.strftime("%b %d %Y %H:%M:%S")
            #print(calcul_temps_TP.time_out)
            now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            #print(now)
            if now > calcul_temps_TP.time_out:
                messages.warning(request, 'Le temps de TP  s\'est écoulé')
                return redirect('students:quiz_list')
            else:
                time_left = calcul_temps_TP.time_out - now
                time_left_scnd = time_left.seconds
        elif target == False :
            #time_init = now
            now = datetime.utcnow().replace(tzinfo=pytz.UTC)
            time_init = now
            time_out = now + timedelta(seconds=60 * Planning.time_TP)
            calcul_temps_TP_left.objects.create(id_usr= request.user.pk, id_TP=pk, time_init=time_init, time_out=time_out,
                                       time_TP=Planning.time_TP)
            time_left = time_out - now
            time_left_scnd = time_left.seconds
            if time_left_scnd > 60 * Planning.time_TP:
                time_left_scnd = 60 * Planning.time_TP
            #print('done --------- ')


        #time_now = now.strftime("%b %d %Y %H:%M:%S")

        """
        elif (m1[0] == request.user.pk) and ( now  < datetime.strptime(m1[2], '%b %d %Y %H:%M:%S') )  :
             time_left =  datetime.strptime(m1[2], '%b %d %Y %H:%M:%S') - now
             time_left_scnd = time_left.seconds
        """
        # fine tompiratory  ( tomporery)
            
            
    





        ## Planning









        if request.method == 'POST':
            #form = TakeQuizForm(question=question, data=request.POST)
            form = correction_TP_Form(request.POST , request.FILES)




            if form.is_valid() :




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
                        messages.info(request, mark_safe(
                            """ <a href='https://docs.google.com/forms/d/1vj-Tw9lid322ENg7AqYMKl7kqnQupfVgU0sIANoOTk8/edit?ts=5f5cc2bc&gxids=7628' target="blank" > اضغط هنا</a> الرجاء الاجابة على أسئلة هذا الاستبيان"""))

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
    else :
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
    print(all_postes_.fiche_tp)
    if '.docx' in  str(all_postes_.fiche_tp) :
        type_fiche = 'application/docx'
    else :
        type_fiche = 'application/pdf'
    try:
        return FileResponse(open(path_pdf, 'rb'), content_type=type_fiche)
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
