from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Question, Answer
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'EasyPoll/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-published_date')[:1]

class QuestionView(generic.DetailView):
    model = Question
    template_name = 'EasyPoll/question.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'EasyPoll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.answer_set.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'EasyPoll/question.html', {'question_detail':question, 'error_message':'Please choose'})

    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('EasyPoll:results', args=(question_id,)))