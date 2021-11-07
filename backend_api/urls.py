from django.urls import path
from .views import LeaveSession, SessionView, CreateSession, GetSessionView, DeleteSessionView, AskQuestion, QuestionView, ValidateLogin, UserView, JoinSession, LeaveSession, InSession, SessionActive
# DeleteSessionView

urlpatterns = [
    path('session', SessionView.as_view()),
    path('create-session', CreateSession.as_view()),
    path('get-session', GetSessionView.as_view()),
    path('delete', DeleteSessionView.as_view()),
    path('ask-question', AskQuestion.as_view()),
    path('questions', QuestionView.as_view()),
    path('validate-host', ValidateLogin.as_view()),
    path('users', UserView.as_view()),
    path('join-session', JoinSession.as_view()),
    path('leave-session', LeaveSession.as_view()),
    path('in-session', InSession.as_view()),
    path('active-session', SessionActive.as_view())
]