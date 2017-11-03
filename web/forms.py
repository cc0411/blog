#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django.forms import forms as django_forms
from django.forms import  fields as django_fields
from django.forms import widgets as django_widgets
from web import models

class BaseForm(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BaseForm, self).__init__(*args, **kwargs)


class SendMsgForm(BaseForm,django_forms.Form):

    email = django_fields.EmailField()

class RegisterForm(BaseForm,django_forms.Form):
    username = django_fields.CharField( max_length=15,
        min_length=3,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于3个字符", 'max_length': "用户名长度不能大于15个字符"}
    )
    email = django_fields.EmailField(error_messages={'required': '用户名不能为空.','invalid': '格式错误',} )
    password = django_fields.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{12,32}$',
        min_length=6,
        max_length=32,
        error_messages={'required': '密码不能为空.', 'invalid': '密码必须包含数字，字母、特殊字符', 'min_length': "密码长度不能小于6个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    email_code = django_fields.CharField()
class  LoginForm(BaseForm,django_forms.Form):
    username = django_fields.CharField()
    password = django_fields.CharField()
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )
    rmb = django_fields.IntegerField(required=False)
