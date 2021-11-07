from django.db import models
from django.db.models.base import Model
import random 
import string

def get_unique_key():
    length = 8
    while True:
        session_code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Session.objects.filter(session_code = session_code).count() == 0:
            break
    return session_code


# Create your models here.
class Session(models.Model):
    session_code = models.CharField(max_length=8, default=get_unique_key, unique=True)
    host = models.CharField(max_length=50, unique=True)
    num_participants = models.IntegerField(null=False, default=0)
    num_questions = models.IntegerField(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class User(models.Model):
    user_id = models.CharField(max_length=50, null=False)
    session_code = models.CharField(max_length=8, null=False)

class Questions(models.Model):
    session_code = models.CharField(max_length=8, null=False)
    content = models.CharField(max_length=350)
    answered = models.BooleanField(default=False)
    topic = models.CharField(max_length=30, null=False)
    answer = models.CharField(max_length=350, null=False)
    created_at = models.DateTimeField(auto_now_add=True)