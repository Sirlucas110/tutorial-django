from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def index(request):
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
