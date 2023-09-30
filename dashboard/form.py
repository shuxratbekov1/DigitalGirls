from django import forms
from .models import *


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['course']


class QuestionResponseForm(forms.ModelForm):
    class Meta:
        model = QuestionResponse
        fields = "__all__"
