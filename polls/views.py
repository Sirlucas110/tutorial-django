from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.views import generic

from datetime import timedelta
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]
    
     
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request=request,
            template_name="polls/detail.html",
            context=
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

#def index(request):
    # Obtém a data e hora atual no fuso horário do Django (pode ser importante se estiver usando timezone-aware datetimes)
    hoje = timezone.now()

    # Calcula a data correspondente a 7 dias atrás a partir de hoje
    semana_passada = hoje - timedelta(days=7)

    # Busca as 5 perguntas mais recentes ordenadas pela data de publicação (do mais recente pro mais antigo)
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    # Filtra todas as perguntas que foram publicadas nos últimos 7 dias (de semana_passada até hoje)
    perguntas = Question.objects.filter(pub_date__range=(semana_passada, hoje))

    # Conta quantas perguntas foram publicadas nesse intervalo de tempo
    quantidade = perguntas.count()

    # Prepara os dados que serão enviados para o template 'index.html'.
    # latest_question_list: lista das 5 perguntas mais recentes
    # quantidade: número total de perguntas publicadas nos últimos 7 dias
    context = {
        "latest_question_list": latest_question_list,
        "quantidade": quantidade
    }

    # Renderiza o template 'polls/index.html' com o contexto acima
    return render(request, "polls/index.html", context)
