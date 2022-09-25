from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Question, Choice

""" zastępujemy go renderem jak powyżej """
from django.template import loader
from polls.models import Question, Choice

# Create your views here.

""" tę funkcję index zastępuemy renederem"""
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:6]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

""" ten inddex zastępuje powyższy 0- jest krócej napisany"""


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:6]


def home(request):
    return HttpResponse("Hello, world. You're at the project homepage.")


""" zastępujmy funkcję detail nowym"""
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})


""" zastepujemy formularzem ??? """

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

""" zastępujemy nowym results,
który pozwoli na zliczanie głosów i powrót do głosowania"""
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)

""" ten rtesults pozwala na na zliczanie głosów i powrót do głosowania"""
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


""" zastepujemy powyższe formularzem ??? """


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # zapytanie dla Queestion w bazie danych dla id
    # jak jest to wykona jak nie ma  to bład 404
    question = get_object_or_404(Question, pk=question_id)
    try:
        # question.choice_set.get - pobniera wszystkie możliwe odpowiedzi
        # pk=request.POST['choice'] - konkretna wybrana dpwoedź - -kliknioęcie VOTE
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))