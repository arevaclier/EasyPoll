from django.conf.urls import url
from . import views

app_name = 'EasyPoll'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.QuestionView.as_view(), name='question'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^add/$', views.addpoll, name='addpoll'),
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^author/$', views.AuthorView.as_view(), name='author'),
    #REST API
    url(r'^api/v1/questions/$', views.APIQuestionList.as_view(), name='question_collection'),
    url(r'^api/v1/questions/(?P<pk>[0-9]+)$', views.APIQuestionSingle.as_view(), name='question_single'),
    url(r'^api/v1/questions/(?P<pk>[0-9]+)/answers/$', views.APIQuestionAnswers.as_view(), name='question_answer_list'),
    url(r'^api/v1/questions/([0-9]+)/answers/(?P<pk>[0-9]+)$', views.APIAnswerSingle.as_view(), name='question_answer_single'),
    url(r'^api/v1/answers/$', views.APIAnswerList.as_view(), name='answer_collection'),
    url(r'^api/v1/answers/(?P<pk>[0-9]+)$', views.APIAnswerSingle.as_view(), name='answer_single')
]