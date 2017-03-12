# -*- coding: utf-8 -*-
import datetime

import math
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from olymp.forms import OlympForm, LoginForm, ProblemInBankForm, ProblemInOlympForm
from olymp.models import Olymp, ProblemInBank, Man, Work


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def getSpec(request):
    if not request.user.is_authenticated:
        return 0
    if request.user.is_superuser:
        return 2
    return sign(len(list((Man.objects.get(user=request.user).ecspertType.all()))))


def subdict(form, keyset):
    return dict((k, form.cleaned_data[k]) for k in keyset)


def olympList(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = OlympForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["date"] = datetime.datetime.today()
            ol = Olymp.objects.create(**d)
            ol.save()

    arr = []
    for l in Olymp.objects.all():
        arr.append({
            "name": l.name,
            "date": l.date,
            "id": l.pk,
            "isParticipated": Work.objects.filter(student=Man.objects.get(user=request.user), olymp=l)
        })

    return render(request, "olymp/olympList.html", {
        'login_form': LoginForm(),
        'eqs': arr,
        'form': OlympForm(),
        'isSpec': getSpec(request)
    })


def participateOlymp(request, olymp_id):
    o = Olymp.objects.get(pk=olymp_id)
    man = Man.objects.get(user=request.user)
    w = Work.objects.create(olymp=o, student=man)
    w.save()
    w.fillOlymp()

    return HttpResponseRedirect('/olymp/list/')


def olympDetail(request, olymp_id):
    ProblemFormset = formset_factory(ProblemInOlympForm)

    eq = Olymp.objects.get(pk=olymp_id)

    if request.method == 'POST':
        problem_formset = ProblemFormset(request.POST, request.FILES, prefix='problem')
        eq.addFromFormset(problem_formset, True)

        # строим форму на основе запроса
        form = OlympForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "date"))
            Olymp.objects.filter(pk=olymp_id).update(**d)

        return HttpResponseRedirect('/olymp/list/')

    c = {'problem_formset': ProblemFormset(initial=eq.generateDataFromProblemStructs(), prefix='problem'),
         'login_form': LoginForm(),
         'one': '1',
         'form': OlympForm(instance=eq, prefix="main_form"),
         'isSpec': getSpec(request),
         }

    return render(request, "olymp/olympDetail.html", c)


def problemList(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ProblemInBankForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "prType"))
            pr = ProblemInBank.objects.create(**d)
            pr.save()
            return HttpResponseRedirect('/problem/detail/' + str(pr.pk) + '/')

    arr = []
    for l in ProblemInBank.objects.all():
        arr.append({
            "name": l.name,
            "prType": l.prType,
            "id": l.pk,
            "text": l.text[:100] + "..."
        })

    return render(request, "olymp/problemList.html", {
        'login_form': LoginForm(),
        'eqs': arr,
        'form': ProblemInBankForm(),
        'isSpec': getSpec(request),
    })


def problemDetail(request, problem_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ProblemInBankForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "prType", "text"))
            ProblemInBank.objects.filter(pk=problem_id).update(**d)

        return HttpResponseRedirect('/problem/list/')

    c = {'login_form': LoginForm(),
         'form': ProblemInBankForm(instance=ProblemInBank.objects.get(pk=problem_id), prefix="main_form"),
         'isSpec': getSpec(request),
         }

    return render(request, "olymp/problemDetail.html", c)


def problemDelete(request, problem_id):
    eq = ProblemInBank.objects.get(pk=problem_id)
    eq.delete()
    return HttpResponseRedirect('/problem/list/')


def workList():
    return None


def loadWork():
    return None


def resultOlymp(request, olymp_id):
    eq = Olymp.objects.get(pk=olymp_id)
    if len(Work.objects.filter(student=Man.objects.get(user=request.user), olymp=eq)) > 0:
        flg = True
        work = Work.objects.get(student=Man.objects.get(user=request.user), olymp=eq)
        marks = work.getMarks()
    else:
        flg = False
        marks = []

    c = {
        'flg': flg,
        'marks': marks,
        'flgChecked': work.checkReady(),
        'isSpec': getSpec(request),
    }
    return render(request, "olymp/olympResult.html", c)
