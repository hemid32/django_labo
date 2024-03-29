
from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('quiz/Compt_rendu/<int:id>', students.pdf_view, name='pdf_view'),
        path('test', students.test_redirect, name='test_view'),
        path('quiz/Compt_rendu/<int:id>/data=<str:r>', students.get_vr, name='get_vr'),
        path('like', students.like,  name='like_h' ),
        path('quiz/Compt_rendu_corct/', students.pdf_corect, name='pdf_corect_ens'),

                               ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/Compt_rendu_corct/', teachers.pdf_corect, name='pdf_corect'),

        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
        path('TP/<int:pk>/', teachers.take_tp_teacher, name='take_tp_teacher'),

                               ], 'classroom'), namespace='teachers')),
]
