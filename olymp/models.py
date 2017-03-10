# -*- coding: utf-8 -*-
import datetime

import django
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models


class ProblemType(models.Model):
    name = models.CharField(default="", max_length=200)

    def __str__(self):
        return self.name


class University(models.Model):
    long = models.CharField(default="", max_length=1000)
    short = models.CharField(default="", max_length=100)

    def __str__(self):
        return self.short

    def __unicode__(self):
        return self.short


class Man(models.Model):
    user = models.OneToOneField(User)
    # отчество
    patronymic = models.CharField(max_length=200)
    # университет
    university = models.ForeignKey(University)
    # экспертом чего является
    ecspertType = models.ManyToManyField(ProblemType, blank=True, default=None)

    def __str__(self):
        return str(self.user) + "(" + str(self.university) + ")"

    def __unicode__(self):
        return str(self.user) + "(" + str(self.university) + ")"


class ProblemInBank(models.Model):
    name = models.CharField(default="", max_length=200)
    text = models.CharField(default="", max_length=20000)
    prType = models.ForeignKey(ProblemType)

    def __str__(self):
        return self.name + " (" + self.text[:40] + "...)"

    def __unicode__(self):
        return self.name + " (" + self.text[:40] + "...)"


class ProblemInOlymp(models.Model):
    number = models.IntegerField(default=1)
    pInB = models.ForeignKey(ProblemInBank)

    def __str__(self):
        return str(self.number) + ". " + str(self.pInB)

    def __unicode__(self):
        return str(self.number) + ". " + str(self.pInB)


class Mark(models.Model):
    val = models.FloatField(default=0.0)
    author = models.ForeignKey(Man)

    def __str__(self):
        return str(self.val) + "(" + str(self.author) + ")"

    def __unicode__(self):
        return str(self.val) + "(" + str(self.author) + ")"


class ProblemInOlympWithMark(models.Model):
    problem = models.ForeignKey(ProblemInOlymp)
    mark = models.ManyToManyField(Mark, blank=True, default=None)

    def __str__(self):
        return str(self.mark) + "(" + str(self.problem) + ")"

    def __unicode__(self):
        return str(self.mark) + "(" + str(self.problem) + ")"


class Olymp(models.Model):
    name = models.CharField(default="", max_length=200)
    date = models.DateField(default=django.utils.timezone.now)
    problems = models.ManyToManyField(ProblemInOlymp, blank=True, default=None)

    def __str__(self):
        return self.name + "(" + str(self.date) + ")"

    def __unicode__(self):
        return self.name + "(" + str(self.date) + ")"

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for pr in self.problems.all():
                pr.delete()
            self.problems.clear()
        if formset.is_valid():
            i = 1

            for form in formset.forms:
                if (form.cleaned_data["pInB"] is not None):
                    pr = ProblemInOlymp.objects.create(number=i,
                                                       pInB=form.cleaned_data["pInB"])
                    pr.save()
                    i += 1
                    self.problems.add(pr)

    def generateDataFromProblemStructs(self):
        arr = []
        for pr in self.problems.all():
            arr.append({'pInB': pr.pInB,
                        'number': pr.number,
                        })

        return arr


fs = FileSystemStorage(location='/media/photos')


class Work(models.Model):
    olymp = models.ForeignKey(Olymp)
    problems = models.ManyToManyField(ProblemInOlympWithMark)
    scan = models.FileField(storage=fs)

    def __str__(self):
        return "(" + str(self.olymp) + ")"

    def __unicode__(self):
        return "(" + str(self.olymp) + ")"
