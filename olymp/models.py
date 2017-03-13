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

    MAX_DELTA = 10

    def getFinalMark(self):
        if len(self.mark.all()) == 0:
            return -1
        else:
            sum = 0
            for m in self.mark.all():
                sum += m.val
            res = float(float(sum) / len(self.mark.all()))
            return res

    def checkReady(self):

        if len(self.mark.all()) < 2:
            return False
        else:
            if len(self.mark.all()) == 2:
                return self.mark.first().val - self.mark.last().val < self.MAX_DELTA
            else:
                return True

    def checkMarkByAuthor(self, man):
        for m in self.mark.all():
            if m.author == man:
                return True
        return False

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


class CMSFileField(models.FileField):
    def pre_save(self, model_instance, add):
        file = super(models.FileField, self).pre_save(model_instance, add)

        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save('%s.pdf' % model_instance.pk, file, save=False)
        return file


class Work(models.Model):
    olymp = models.ForeignKey(Olymp, blank=True, default=None)
    problems = models.ManyToManyField(ProblemInOlympWithMark, blank=True, default=None)
    scan = CMSFileField(upload_to='./works/', blank=True, default=None)
    student = models.ForeignKey(Man, blank=True, default=None)

    def generateData(self, man):
        arr = []
        for pr in self.problems.all():
            flg = True
            tm = None
            for mark in pr.mark.all():
                if mark.author == man:
                    tM = mark
                    flg = False
            if flg:
                m = Mark.objects.create(author=man)
                m.save()
                tM = m
                pr.mark.add(m)
            arr.append({'problem': pr.problem,
                        'mark': tM.val,
                        'wId': self.pk,
                        })
        return arr

    def __str__(self):
        return "(" + str(self.olymp) + ")"

    def __unicode__(self):
        return "(" + str(self.olymp) + ")"

    def getMarks(self):
        arr = []
        for p in self.problems.all():
            if p.getFinalMark() == -1:
                return []
            else:
                tmp = []
                tmp.append(p.problem.number)
                tmp.append( p.getFinalMark())
                arr.append(tmp)
        return arr

    def getSum(self):
        sm = 0
        for m in self.getMarks():
            sm += m[1]

        return sm

    def fillOlymp(self):
        for p in self.olymp.problems.all():
            pwm = ProblemInOlympWithMark.objects.create(problem=p)
            pwm.save()
            self.problems.add(pwm)

    def checkReady(self):
        for p in self.problems.all():
            if not p.checkReady():
                return False
        return True

    def addFromFormset(self, formset, man):
        if formset.is_valid():
            i = 1
            for form in formset.forms:
                if len(form.cleaned_data) > 0:
                    p = ProblemInOlympWithMark.objects.get(problem=form.cleaned_data['problem'],
                                                           work=Work.objects.get(pk=int(form.cleaned_data['wId'])))
                    m = p.mark.all().filter(author=man).first()

                    m.val = form.cleaned_data['mark']
                    m.save()
                    print(form.cleaned_data['mark'])


    def checkMarkByAuthor(self, man):
        for p in self.problems.all():
            if p.checkMarkByAuthor(man):
                return False

        return True
