# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin

import olymp.views
import olymp.auth


admin.autodiscover()

urlpatterns = [
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
    url(r'^logout/$', olymp.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', olymp.auth.register),
    url(r'^olymp/list/$', olymp.views.olympList),
    url(r'^olymp/participate/(?P<olymp_id>[0-9]+)/$', olymp.views.participateOlymp),
    url(r'^olymp/result/(?P<olymp_id>[0-9]+)/$', olymp.views.resultOlymp),
    url(r'^olymp/detail/(?P<olymp_id>[0-9]+)/$', olymp.views.olympDetail),
    url(r'^problem/list/$', olymp.views.problemList),
    url(r'^work/list/$', olymp.views.workList),
    url(r'^work/load/$', olymp.views.loadWork),
    url(r'^work/vote/(?P<work_id>[0-9]+)/$', olymp.views.voteWork),
    url(r'^work/getScan/(?P<work_id>[0-9]+)/$', olymp.views.getWorkScan),
    url(r'^problem/detail/(?P<problem_id>[0-9]+)/$', olymp.views.problemDetail),
    url(r'^problem/delete/(?P<problem_id>[0-9]+)/$', olymp.views.problemDelete),
    url(r'^', olymp.auth.index, name='index'),

]