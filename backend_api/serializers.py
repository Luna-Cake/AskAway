from rest_framework import serializers
from .models import Session, Questions, User

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'session_code', 'host', 'num_participants', 'num_questions', 'created_at')

class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session 
        fields = ()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'session_code', 'topic', 'content', 'answer', 'answered', 'created_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_id', 'session_code')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'session_code')

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('session_code', 'topic', 'content')
