from django import forms
from .models import Question, Answer


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('q_text',)


    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['q_text'].label = 'Question'


class AddAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('a_text',)

        def __init__(self, *args, **kwargs):
            super(forms.ModelForm, self).__init__(*args, **kwargs)
            self.fields['a_text'].label = 'Answer'

