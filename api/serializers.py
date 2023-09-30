from rest_framework import serializers
from dashboard.models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class RegisteredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredUser
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"


class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ('candidate', 'percentage')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Question
        exclude = ['correct_answer']
