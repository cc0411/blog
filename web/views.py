#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from io import  BytesIO
import json
from utils.check_code import create_validate_code
from forms import LoginForm,SendMsgForm,RegisterForm
from web import  models
from django.db.models import Q
import datetime
from utils import commons

# Create your views here.


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream,"PNG")
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())
def send_msg(request):
    result = {'status': False, 'message': None, 'data': None}
    form = SendMsgForm(request=request, data=request.POST)
    if request.method=='POST':
        if form.is_valid():
            _value_dict = form.clean()
            email = _value_dict['email']
            has_exists_email = models.UserInfo.objects.filter(email=email).count()
            if has_exists_email:
                result['message'] = '此邮箱已被注册'
                return  HttpResponse(json.dumps(result))
            current_date = datetime.datetime.now()
            code = commons.random_code()
            count = models.SendMsg.objects.filter(email=email).count()
            if not count:
                models.SendMsg.objects.create(code=code, email=email, ctime=current_date)
                result['status'] = True
            else:
                limit_day = current_date - datetime.timedelta(hours=1)
                times = models.SendMsg.objects.filter(email=email, ctime__gt=limit_day, times__gt=9).count()
                if times:
                    result['message'] = "'已超最大次数（1小时后重试）'"
                else:
                    unfreeze = models.SendMsg.objects.filter(email=email, ctime__lt=limit_day).count()
                    if unfreeze:
                        models.SendMsg.objects.filter(email=email).update(times=0)

                    from django.db.models import F

                    models.SendMsg.objects.filter(email=email).update(code=code,
                                                                      ctime=current_date,
                                                                      times=F('times') + 1)
                    result['status'] = True
    else:
        result['message'] = form.errors['email'][0]
    return  HttpResponse(json.dumps(result))
def register(request):

    if request.method == "GET":
        return render(request,'register.html')
    elif request.method == 'POST':
        result = {'status': False, 'message': None, 'data': None}
        form = RegisterForm(request=request, data=request.POST)
        if form.is_valid():
            current_date = datetime.datetime.now()
            limit_day = current_date - datetime.timedelta(minutes=1)
            _value_dict = form.clean()
            is_valid_code = models.SendMsg.objects.filter(email=_value_dict['email'],
                                                          code=_value_dict['email_code'],
                                                          ctime__gt=limit_day).count()
            if not is_valid_code:
                result['message'] = '邮箱验证码不正确或过期'
                return HttpResponse(json.dumps(result))
            has_exists_email = models.UserInfo.objects.filter(email=_value_dict['email']).count()
            if has_exists_email:
                result['message'] = '邮箱已经存在'
                return  HttpResponse(json.dumps(result))
            has_exists_username = models.UserInfo.objects.filter(username=_value_dict['username']).count()
            if has_exists_username:
                result['message'] = '用户名已经存在'
                return HttpResponse(json.dumps(result))
            _value_dict['ctime'] = current_date
            _value_dict.pop('email_code')
            obj = models.UserInfo.objects.create(**_value_dict)
            user_info_dict = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}
            models.SendMsg.objects.filter(email=_value_dict['email']).delete()
            request.session['is_login'] = True
            request.session['user_info'] = user_info_dict
            result['status'] = True
        else:
            error_msg = form.errors.as_json()
            result['message'] = json.loads(error_msg)
        return  HttpResponse(json.dumps(result))


def auth_login(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return inner


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method =='GET':
        return render(request,'login.html')
    elif request.method =='POST':
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            _value_dict = form.clean()
            if _value_dict['check_code'].lower() != request.session["CheckCode"].lower():
                result['message'] = '验证码错误'
                return HttpResponse(json.dumps(result))
            con = Q()
            q1 = Q()
            q1.connector = 'AND'
            q1.children.append(('email',_value_dict['username']))
            q1.children.append(('password',_value_dict['password']))
            q2 = Q()
            q2.connector = 'AND'
            q2.children.append(('username',_value_dict['username']))
            q2.children.append(('password',_value_dict['password']))
            con.add(q1, 'OR')
            con.add(q2, 'OR')
            print _value_dict['username'],_value_dict['password']
            user_info = models.UserInfo.objects.filter(con).first()
            if not user_info:
                result['message'] ='用户名或者密码错误'
                return HttpResponse(json.dumps(result))
            else:
                result['status'] = True
                request.session['is_login'] = True
                request.session['user_info'] = {'nid':user_info.nid,'username':user_info.username,'email':user_info.email,'nickname':user_info.nickname}
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            error_msg = form.errors.as_json()
            print error_msg
            #result['message'] = json.loads(error_msg)
            result['message'] = '123'
        return  HttpResponse(json.dumps(result))

def logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/login')
@auth_login
def index(request):
    return HttpResponse('OK')






































