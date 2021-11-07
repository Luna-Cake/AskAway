from django.db.models import query
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Questions, Session, User
from .serializers import SessionSerializer, CreateSessionSerializer, CreateQuestionSerializer, QuestionSerializer, UserSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.
class SessionView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class CreateSession(APIView):
    serializer_class = CreateSessionSerializer
    
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            host = self.request.session.session_key
            query_set = Session.objects.filter(host=host)

            if query_set.exists():
                session = query_set[0]
            else:
                session = Session(host=host)
                session.save()
            return Response(SessionSerializer(session).data, status=status.HTTP_200_OK)

class GetSessionView(generics.ListAPIView):
    serializer_class = SessionSerializer

    def get(self, request, format=None):
        session_code = request.GET.get('session_code')
        if session_code != None:
            queryset = Session.objects.filter(session_code=session_code)
            if len(queryset) > 0:
                data = SessionSerializer(queryset[0]).data
                data['is_host'] = self.request.session.session_key == queryset[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Error": "Invalid room code."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Error": "No room code specified."}, status=status.HTTP_400_BAD_REQUEST)

class DeleteSessionView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = CreateSessionSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            host = self.request.session.session_key

            sessions = Session.objects.filter(host=host)
            if len(sessions) > 0:
                session = sessions[0]
                users = User.objects.filter(session_code=session.session_code)
                for user in users:
                    user.delete()
                session.delete()
                return Response({"Success": "Successfully deleted record."}, status=status.HTTP_200_OK)
            return Response({"Success": "Nothing to delete."}, status=status.HTTP_200_OK)

class ValidateLogin(APIView):
    serializer_class = SessionSerializer

    def get(self, request, format=None):
        session_code = request.GET.get('session_code')
        session = Session.objects.filter(session_code=session_code)

        if len(session) > 0:
            data = SessionSerializer(session[0]).data
            if session[0].host == self.request.session.session_key:
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Error": "Invalid authorization"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"Error": "Session code not found."}, status=status.HTTP_404_NOT_FOUND)

class JoinSession(APIView):
    serializer_class = SessionSerializer
    user_serializer = UserSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        session_code = request.GET.get('session_code')
        sessions = Session.objects.filter(session_code=session_code)

        if len(sessions) > 0:
            user = User.objects.filter(user_id=self.request.session.session_key)
            user_host = Session.objects.filter(host=self.request.session.session_key)
            if len(user) > 0 or len(user_host) > 0:
                return Response({"Error": "Already part of an existing session."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                session = sessions[0]
                session.num_participants += 1
                session.save(update_fields=['num_participants'])

                new_user = User(session_code=session_code, user_id=self.request.session.session_key)
                new_user.save()

                return Response(SessionSerializer(session).data, status=status.HTTP_200_OK)

        return Response({"Error": "Session code not found."}, status=status.HTTP_404_NOT_FOUND)

class LeaveSession(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        session_code = request.GET.get('session_code')
        sessions = Session.objects.filter(session_code=session_code)

        if len(sessions) == 0:
            return Response({"Error": "Session code not found."}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(user_id=self.request.session.session_key)

        if len(user) > 0:
            session = sessions[0]
            session.num_participants -= 1
            session.save(update_fields=['num_participants'])
            user.delete()
            return Response({"Success": "Left session successfully."}, status=status.HTTP_200_OK)
        return Response({"Error": "User is not part of an existing session."}, status=status.HTTP_404_NOT_FOUND)

class InSession(APIView):
    def get(self, request, format=None):
        session_key = self.request.session.session_key

        sessions = User.objects.filter(user_id=session_key)

        if len(sessions) > 0:
            session = UserSerializer(sessions[0]).data
            session['is_host'] = False
            return Response(session, status=status.HTTP_200_OK)

        host_sessions = Session.objects.filter(host=session_key)

        if len(host_sessions) > 0:
            session = SessionSerializer(host_sessions[0]).data
            session['is_host'] = True
            return Response(session, status=status.HTTP_200_OK)
        
        return Response({"Status": "Not in room"}, status=status.HTTP_404_NOT_FOUND)

class SessionActive(APIView):
    def get(self, request, format=None):
        session_code = request.GET.get('session_code')

        sessions = Session.objects.filter(session_code=session_code)

        if len(sessions) > 0:
            return Response({"Status": "Session is active."}, status=status.HTTP_200_OK)
        return Response({"Status": "Session is inactive."}, status=status.HTTP_404_NOT_FOUND)

class QuestionView(generics.ListAPIView):
    queryset = Questions.objects.all()
    serializer_class = QuestionSerializer

class AskQuestion(APIView):
    serializer_class = CreateQuestionSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            topic = serializer.data.get('topic')
            content = serializer.data.get('content')
            session_code = serializer.data.get('session_code')

            query_set = Questions.objects.filter(content=content).filter(session_code=session_code)

            if len(query_set) > 0:
                return Response({"Error": "Question already exists."}, status=status.HTTP_409_CONFLICT)
            else:
                question = Questions(topic=topic, content=content, session_code=session_code)
                question.save()

            return Response(CreateQuestionSerializer(question).data, status=status.HTTP_200_OK)
        return Response({"Error": "Invalid format."}, status=status.HTTP_400_BAD_REQUEST)

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer