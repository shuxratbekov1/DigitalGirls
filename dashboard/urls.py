from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', Index, name='index'),
    path('course/', CourseView, name='course'),

    path('search/', SearchView, name='search'),
    path('searchResult/<int:pk>/', SearchResultView, name='searchResult'),

    path('userAnswerCoursePage/', UserAnswerCoursePage, name='userAnswerCoursePage'),
    path('userAnswerListPage/<int:pk>/', UserAnswerListPage, name='userAnswerListPage'),
    path('userAnswerQuestionViewPage/<int:pk>/', UserAnswerQuestionViewPage, name='userAnswerQuestionViewPage'),

    path('questionList/<int:pk>/', QuestionList, name='questionList'),
    path('questionAdd/<int:pk>/', QuestionAdd, name='questionAdd'),
    path('deleteQuestion/<int:pk>/', DeleteQuestion, name='deleteQuestion'),

    path('candidateList/', CandidateList, name='candidateList'),

    path('', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),

    path('studied/', studiedView, name='studied'),
    path('registered/', registeredView, name='registered'),
    path('registered/detail/<int:pk>/', registeredDetailView, name='registered-detail'),

]
