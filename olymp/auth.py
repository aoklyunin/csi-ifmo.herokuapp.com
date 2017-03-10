# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from olymp.forms import RegisterForm, LoginForm
from olymp.models import Man


def register(request):
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = RegisterForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            data = {'username': form.cleaned_data["username"],
                    'patronymic': form.cleaned_data["patronymic"],
                    'mail': form.cleaned_data["mail"],
                    'name': form.cleaned_data["name"],
                    'second_name': form.cleaned_data["second_name"],
                    'university': form.cleaned_data["university"],
                    }
            # проверяем, что пароли совпадают
            if form.cleaned_data["password"] != form.cleaned_data["rep_password"]:
                # выводим сообщение и перезаполняем форму
                messages.error(request, "пароли не совпадают")
                # перерисовываем окно
                return render(request, "olymp/register.html", {
                    'form': RegisterForm(initial=data),
                    'login_form': LoginForm()
                })
                # проверяем, что пароли совпадают
            if (form.cleaned_data["code"] != "qwe123QWE") and\
                (form.cleaned_data["code"] != "st123") :
                # выводим сообщение и перезаполняем форму
                messages.error(request, "Неверный код доступа")
                # перерисовываем окно
                return render(request, "olymp/register.html", {
                    'form': RegisterForm(initial=data),
                    'login_form': LoginForm()
                })
            if form.cleaned_data["university"] is None:
                # выводим сообщение и перезаполняем форму
                messages.error(request, "Необходимо выбрать университет")
                # перерисовываем окно
                return render(request, "olymp/register.html", {
                    'form': RegisterForm(initial=data),
                    'login_form': LoginForm()
                })

            else:
                try:
                    # создаём пользователя
                    user = User.objects.create_user(username=form.cleaned_data["username"],
                                                    email=form.cleaned_data["mail"],
                                                    password=form.cleaned_data["password"])
                except:
                    messages.error(request, "Такой пользователь уже есть")
                    return render(request, "olymp/register.html", {
                        'form': RegisterForm(initial=data),
                        'login_form': LoginForm()
                    })

                # задаём ему имя и фамилию
                user.first_name = form.cleaned_data["name"]
                user.last_name = form.cleaned_data["second_name"]
                # созраняем пользователя
                user.save()

                # создаём студента
                w = Man.objects.create(user=user, patronymic=form.cleaned_data["patronymic"],
                                       university=form.cleaned_data["university"])

                # сохраняем эксперта
                w.save()
                if (form.cleaned_data["code"] == "qwe123QWE"):
                    for prt in form.cleaned_data["problemTypes"]:
                        w.ecspertType.add(prt)

                return HttpResponseRedirect("/")
        else:
            # перезагружаем страницу
            return HttpResponseRedirect("/")
    else:
        # возвращаем простое окно регистрации
        return render(request, "olymp/register.html", {
            'form': RegisterForm(),
            'login_form': LoginForm()
        })


# выход из системы
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


# стартовая страница
def index(request):
    # обработка входа
    if request.method == "POST":
        # если в post-запросе есть поля логина/пароля
        if ("username" in request.POST) and ("password" in request.POST):
            username = request.POST['username']
            password = request.POST['password']
            # пробуем залогиниться
            user = auth.authenticate(username=username, password=password)
            request.POST._mutable = True
            # если полльзователь существует и он активен
            if user is not None and user.is_active:
                # входим на сайт
                auth.login(request, user)
                # выводим сообщение об удаче
                messages.success(request, "успешный вход")
            else:
                messages.error(request, "пара логин-пароль не найдена")
    template = 'olymp/index.html'
    context = {
        "user": request.user,
        "login_form": LoginForm(),
    }
    return render(request, template, context)
