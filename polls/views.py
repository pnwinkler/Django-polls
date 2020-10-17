from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # context_object_name lets us overwrite the default (automatically generated) name for the context variable. Otherwise, it would be "question_list" 
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last 5 published questions
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    # each generic view needs to know which model it will be acting upon
    # because we're using a Django model (Question), Django automatically determines an appropriate name for the context variable
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # excludes any qiestions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is dictionary like object. Always returns str
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
       # always return an HttpResponseRedirect after successfully dealing with POST data! This prevents data from being posted twice if a user hits the Back button
        # otherwise we'd just use an HttpResponse(...)
        # reverse(...) helps us not hardcode a URL
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
