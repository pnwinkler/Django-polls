from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # we use pk for the next 2 entries because that's what generic.DetailView expects (in polls/views.py)
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # I think this line below is not a generic. That's why the syntax is different.
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

