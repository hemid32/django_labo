from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..decorators import teacher_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm, evaluation_form
from ..models import Answer, Question, Quiz, User, TakenQuiz, Planning_TP, Student
from django.conf import settings
from django.http import HttpResponse, Http404, FileResponse, HttpResponseForbidden
from django.views.generic.edit import FormMixin
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:quiz_change_list')


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/teachers/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject','type_tp', 'module' , 'Temps_TP',)
    template_name = 'classroom/teachers/quiz_add_form.html'






    def form_valid(self, form):


        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        #Plannig
        #usr_id = User.objects.filter(is_student=True).values('id')
        student  =  Student.objects.filter(interests = quiz.subject).values('user_id')


        ta = 0
        for i in student :
            # print(i['id'])
            time_in = datetime.now() + timedelta(minutes= 60*ta)
            time_fn = time_in + timedelta(minutes=60*12)
            temps_tp = quiz.Temps_TP
            id_usr = i['user_id']
            id_tp = quiz.pk
            #print(time_in, time_fn, id_usr , id_tp , temps_tp )
            Planning_TP.objects.create(id_usr = id_usr , id_TP = id_tp , time_in = time_in , time_fn = time_fn , time_TP = temps_tp)
            #Planning_TP.save()
            ta += 12
            # ##############   imail
            student_email = User.objects.get(pk=i['user_id'])
            email_student = student_email.email
            # print('email =====', email_student)
            try:
                time_in = time_in.strftime("%b %d %Y %H:%M:%S")
                time_fn = time_fn.strftime("%b %d %Y %H:%M:%S")
                subject, from_email, to = 'Un nouveau travail pratique vous attend', 'laboratoir.elbayadh@gmail.com', email_student
                text_content = 'This is an important message.'
                html_content = '''<p>Bonjour <strong>{nome} {nome2}</strong> <br> Vous avez un nouveau travail appliqué qui vous attend .Selon le calendrier, votre date de réalisation  tp est : 
                                                <br>Du <strong> {date_in} </strong>  Au <strong>{date_fn} </strong>  <br> Temps consacré aux travaux pratiques : 
                                               <strong> {temps_TP} minit </strong> <br>  Assurez-vous de respecter le calendrier  <br> 
                                                  <strong> LABTEC </strong></p>'''.format(nome=student_email.first_name, date_in=time_in,
                                                                                          date_fn=time_fn, temps_TP=str(temps_tp),
                                                                                          nome2=student_email.last_name)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                pass
            ################   imail
        #Planning
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('teachers:quiz_change', quiz.pk)


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', 'type_tp' , 'module' )

    '''
    def get_form(self, form_class= Quiz):
        form = form_class()
        form.fields['subject'].label = "Primary purpose/business use"
        #form.fields['secondary_purpose_business_uses'].label = "Secondary purpose/business uses"

        return form
    '''

    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_change_form.html'



    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        #self.fields['subject'].label = 'classe'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})




@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_delete_confirm.html'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(FormMixin,DetailView):

    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_results.html'
    form_class = evaluation_form

    def get_success_url(self):
        return reverse('teachers:quiz_results', kwargs={'pk': Quiz.pk})

    #return reverse('author-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        Planning =Planning_TP.objects.all()
        student = Student.objects.all()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('compte_rendu'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score,
            'form': evaluation_form(initial={'post': self.object}) ,
            'planning' : Planning ,
            'student' : student ,
        }

        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)



    def get_queryset(self):
        return self.request.user.quizzes.all()


    def post(self, request, *args, **kwargs):
        #print('POOOOOOOOOOOOOOOOOOOOOST')

        self.object = self.get_object()
        form = self.get_form( )
        note = request.POST['note']
        ID_std = request.POST['std_user_Id']
        ID_TP = request.POST['TP_Id']
        try:
            file_correction_ens = request.FILES['myfile']
            file  = True
        except :
            file  = False
        #print('yesssssssssssssssssssssssssssssssssss21212121221212121212122112211xxxxx',note ,ID_std  , ID_TP)
        if form.is_valid() and file:
            #return self.form_valid(form)

            #note =  request.POST['note']
            #print('yesssssssssssssssssssssssssssssssssss21212121221212121212122112211xxxxx')

            #return reverse('teachers:quiz_results', Quiz.pk)
            messages.success(self.request, 'Le note a été modifié.')
            quiz = self.get_object()

            print()
            t = TakenQuiz.objects.get(pk = ID_TP , student = ID_std )
            print('student ============ ', t.score)
            t.score = note  # change field
            t.correction_TP_ensegn = file_correction_ens

            t.save()  # this will update only

            return redirect('teachers:quiz_results' ,quiz.pk)

        else:
            if file == False:
                print('11111111111111111111111222222222222222222*********')
                messages.warning(self.request , 'Veuillez ajouter le fichier de correctif !!!')
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()

        return super(QuizResultsView, self).form_valid(form)





@login_required
@teacher_required
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST ,  request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.

    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('teachers:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'classroom/teachers/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'classroom/teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})




########### correction tp
@login_required
@teacher_required
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

