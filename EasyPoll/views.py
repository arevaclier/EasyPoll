from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from .models import Question, Answer
from django.urls import reverse
from django.views import generic
from .forms import AddQuestionForm, AddAnswerForm
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from EasyPoll.serializers import QuestionSerializer, AnswerSerializer
from rest_framework.views import APIView


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

        # Get total number of votes for latest poll
        answers = Answer.objects.filter(question_id=latest_question.id)
        latest_total_votes = 0
        for i in answers:
            latest_total_votes = latest_total_votes + i.votes
        context['latest_poll_votes'] = latest_total_votes

        # Get poll of the month
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

        # Get highest poll ever
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

    def get_context_data(self, *args, **kwargs):
        context = super(ResultsView, self).get_context_data(*args, **kwargs)

        answers = Answer.objects.filter(question_id=self.kwargs['pk'])
        total_votes = 0
        for i in answers:
            total_votes = total_votes + i.votes
        context['poll_votes'] = total_votes
        return context


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.answer_set.get(pk=request.POST['choice'])
    except (KeyError, Answer.DoesNotExist):
        return render(request, 'EasyPoll/question.html',
                      {'question_detail': question, 'error_message': 'Please choose'})

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
        aforms = [AddAnswerForm(prefix=str(x), instance=Answer()) for x in range(0, 3)]

        context = {'qform': qform, 'aforms': aforms}
        return render(request, 'EasyPoll/addpoll.html', context)


class ListView(generic.ListView):
    model = Question
    template_name = 'EasyPoll/list.html'
    context_object_name = 'poll_list'
    paginate_by = 10


class AuthorView(generic.ListView):
    model = Question
    template_name = 'EasyPoll/author.html'
    context_object_name = 'list'
    paginate_by = 10

    def get_queryset(self):
        qs = Question.objects.filter(author=self.request.user)
        return qs


"""
    REST API
"""


class APIQuestionList(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIQuestionSingle(APIView):
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIAnswerList(APIView):
    def get(self, request):
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIAnswerSingle(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        answer = self.get_object(pk)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        answer = self.get_object(pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIQuestionAnswers(APIView):
    def get_object(self, pk):
        try:
            return Answer.objects.select_related().filter(question=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        answers = self.get_object(pk)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

