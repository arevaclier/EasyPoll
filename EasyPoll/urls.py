from django.conf.urls import url
from . import views

app_name = 'EasyPoll'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.QuestionView.as_view(), name='question'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^add/$', views.addpoll, name='addpoll'),
    url(r'^list/$', views.ListView.as_view(), name='list')
]