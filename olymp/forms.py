# -*- coding: utf-8 -*-
from crispy_forms.layout import Layout, Field
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

from olymp.models import University, ProblemInBank, Olymp, ProblemInOlymp, ProblemType, Work


class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма регистрации
class RegisterForm(forms.Form):
    # логин
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес электронной почты")
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")

    # фамилия
    code = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                           label="Код доступа")
    # отчество
    patronymic = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванович'}),
                                 label="Отчество")
    # Университет
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False, label="Университет")
    # Область специализации
    problemTypes = forms.ModelMultipleChoiceField(queryset=ProblemType.objects.all(), required=False,
                                                  label="Специализация*")


class ProblemInBankForm(ModelForm):
    class Meta:
        model = ProblemInBank
        fields = {'name', 'text', 'prType'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 150, 'placeholder': 'Текст задания'})
        }

        labels = {
            'text': 'Текст',
            'prType': 'Вид',
            'name': 'Название',
        }

        error_messages = {
            'text': {'invalid': '', 'invalid_choice': ''},
            'prType': {'required': ''},
            'name': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProblemInBankForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.helper = FormHelper()
        self.fields["text"].required = False

        self.helper.layout = Layout(
            Field('text', css_class='col-sm-8', ),
            Field('prType', css_class='col-sm-2'),
            Field('name', css_class='col-sm-2'))


class OlympForm(ModelForm):
    class Meta:
        model = Olymp
        fields = {'name', 'date'}
        widgets = {

        }

        placeholders = {
            'name': 'Олимпиада ТАУ 2017'
        }
        labels = {
            'name': 'Название',
            'date': 'Дата',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'date': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(OlympForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.helper = FormHelper()
        self.fields["date"].required = False
        self.helper.layout = Layout(
            Field('name', css_class='col-sm-2', ),
            Field('date', css_class='col-sm-2'))


class ProblemInOlympForm(ModelForm):
    class Meta:
        model = ProblemInOlymp
        fields = {'number', 'pInB'}

        widgets = {
        }

        labels = {
            'pInB': '',
            'number': '',
        }

        error_messages = {
            'pInB': {'invalid': '', 'invalid_choice': ''},
            'number': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProblemInOlympForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.helper = FormHelper()
        self.fields["number"].required = False
        self.fields["pInB"].required = False

        self.helper.layout = Layout(
            Field('pInB', css_class='col-sm-8', ),
            Field('number', css_class='col-sm-2'))


# форма загрузки раоты
class WorkLoadForm(forms.Form):
    scan = forms.FileField(label="Скан работы")

    def __init__(self, *args, **kwargs):
        super(WorkLoadForm, self).__init__(*args, **kwargs)
        arr = []
        i = 1
        for w in Work.objects.filter(scan=""):
            arr.append([str(w.pk), str(w.pk)])
            i += 1
        self.fields['workIds'] = forms.ChoiceField(
            choices=arr, label="ID работы"
        )


class ProblemWithMarkForm(forms.Form):
    mark = forms.FloatField(label="Оценка", required=False)
    wId = forms.IntegerField(label="wId",required=False)

    # Университет
    def __init__(self, *args, **kwargs):
        work = kwargs.pop('work')
        super(ProblemWithMarkForm, self).__init__(*args, **kwargs)
        arr = []
        for p in work.problems.all():
            arr.append(p.problem.pk)
        self.fields['problem'] = forms.ModelChoiceField(queryset=ProblemInOlymp.objects.filter(pk__in=arr),
                                                        required=False, label="Задача")
        self.fields['wId'].widget = forms.HiddenInput()