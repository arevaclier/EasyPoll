from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Question, Answer
from django.urls import reverse
from django.views import generic
from .forms import AddQuestionForm, AddAnswerForm
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'EasyPoll/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """Return the last published question."""
        return Question.objects.latest('published_date')

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        latest_question = Question.objects.latest('published_date')

        #Get total number of votes for latest poll
        answers = Answer.objects.filter(question_id=latest_question.id)
        latest_total_votes = 0
        for i in answers:
            latest_total_votes = latest_total_votes + i.votes
        context['latest_poll_votes'] = latest_total_votes

        #Get poll of the month
        last_month = datetime.today() - timedelta(days=30)
        month_polls = Question.objects.filter(published_date__gte=last_month).order_by('-published_date')
        month_poll = None
        total_votes = 0
        for i in month_polls:
            answers = Answer.objects.filter(question_id=i.id)
            votes = 0
            for j in answers:
                votes = votes + j.votes
            if votes >= total_votes:
                month_poll = i
                total_votes = votes
        context['month_poll'] = month_poll
        context['month_poll_votes'] = total_votes

        #Get highest poll ever
        polls = Question.objects.all().order_by('-published_date')
        highest_poll = None
        total_votes = 0
        for i in polls:
            answers = Answer.objects.filter(question_id=i.id)
            votes = 0
            for j in answers:
                votes = votes + j.votes
            if votes >= total_votes:
                highest_poll = i
                total_votes = votes
        context['highest_poll'] = highest_poll
        context['highest_poll_votes'] = total_votes
        return context

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

def addpoll(request):

    if request.method == "POST":
        qform = AddQuestionForm(request.POST)

        aforms = [AddAnswerForm(request.POST, prefix=str(x), instance=Answer()) for x in range(0, 3)]

        if qform.is_valid():
            question = qform.save(commit=False)
            question.author = request.user
            question.published_date = timezone.now()
            question.save()
            poll = Question.objects.latest('published_date')
            for aform in aforms:
                answer = aform.save(commit=False)
                answer.question = poll
                answer.save()
            return redirect('EasyPoll:results', pk=question.pk)

    else:
        qform = AddQuestionForm()
        aforms = [AddAnswerForm(prefix=str(x), instance=Answer()) for x in range(0,3)]

        context = {'qform':qform, 'aforms':aforms}
        return render(request, 'EasyPoll/addpoll.html', context)

class ListView(generic.ListView):
    model = Question
    template_name = 'EasyPoll/list.html'