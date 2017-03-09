# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from olymp.models import ProblemType, Expert, Student, ProblemInBank, Mark, ProblemInOlympWithMark, Olymp, Work, \
    ProblemInOlymp
from olymp.models import University

admin.site.register(ProblemType)
admin.site.register(University)
admin.site.register(Expert)
admin.site.register(Student)
admin.site.register(ProblemInBank)
admin.site.register(Mark)
admin.site.register(ProblemInOlympWithMark)
admin.site.register(ProblemInOlymp)
admin.site.register(Olymp)
admin.site.register(Work)