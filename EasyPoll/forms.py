from django import forms
from .models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('q_text',)


    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['q_text'].label = 'Question'


class AddAnswerForm(forms.ModelForm):
    a_text = forms.CharField(widget=forms.TextInput, label='Answer')
    class Meta:
        model = Answer
        fields = ['a_text']

