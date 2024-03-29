from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import DateInput
from django.forms.utils import ValidationError

from classroom.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User , correction_TP,evaluation_module)



class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'username','email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):

    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name' ,'last_name' ,'date_of_birth' ,'username', 'email','password1', 'password2')



    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)
        self.fields['interests'].label  = 'classe'




    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))


        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('fiche_tp','description')
    """
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['Subject'].label  = 'classe'
    """




class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):

    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer',)
        #fields = ('answer')




    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')

        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class  correction_TP_Form(forms.ModelForm):

    class Meta :
        model = correction_TP
        fields = ( 'compte_rendu', )


class evaluation_form(forms.ModelForm):
    class Meta:
        model = evaluation_module
        fields = ('note',)

