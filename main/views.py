from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from DBwaf.waf_agent import if_text_vulnerable_sql, if_text_vulnerable_xss_from_response, if_text_vulnerable
from connectionWithDockerModel.main import if_xss_text_vulnerable_without_saving_to_logger, \
    if_sql_text_vulnerable_without_saving_to_logger
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template import loader

from main.models import UserDemo

XSS_THRESHOLD = 0.45
SQL_THRESHOLD = 0.5


def set_waf_flag_cookie(request):
    select = request.POST.get('radio')
    if select == 'no_protection':
        request.session['waf_flag'] = False
        request.session['threshold_xss'] = XSS_THRESHOLD
        request.session['threshold_sql'] = SQL_THRESHOLD
        request.session.save()

    elif select == 'protection':
        request.session['waf_flag'] = True
        if request.POST.get('threshold_xss') != '':
            request.session['threshold_xss'] = request.POST.get('threshold_xss')
        if request.POST.get('threshold_sql') != '':
            request.session['threshold_sql'] = request.POST.get('threshold_sql')
        request.session.save()
    return request


def demo_site(request):
    return render(request, template_name='main/base_demo_site.html')


def demo_setting(request):
    context = {}
    request.session['waf_flag'] = False
    request.session['threshold_xss'] = XSS_THRESHOLD
    request.session['threshold_sql'] = SQL_THRESHOLD
    request.session.save()
    request = set_waf_flag_cookie(request)

    if request.method == 'GET':
        if request.session['waf_flag'] is True:
            context = {'message_waf': 'The site is protected by WAF'}
        else:
            context = {'message_waf': 'The site is unprotected by WAF'}

        return render(request, 'main/setting_demo.html', context)

    if request.method == 'POST':

        if request.session['waf_flag'] is False:
            messages.success(request, "The site is unprotected now by WAF")
            context = {'message_waf': 'The site is unprotected by WAF'}
        elif request.session['waf_flag'] is True:
            messages.success(request, "The site is protected now by WAF")
            context = {'message_waf': 'The site is protected by WAF'}

    return render(request, 'main/setting_demo.html', context)


def demo_sql(request):
    if request.method == 'GET':
        if request.session['waf_flag'] is True:
            context = {'message_waf': 'The site is protected by WAF'}
        else:
            context = {'message_waf': 'The site is unprotected by WAF'}
        return render(request, 'main/sql_demo.html', context)

    if request.method == 'POST':
        cur_user = None
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        sql = f"SELECT * FROM main_userdemo WHERE username = '{user_name}' AND password = '{user_password}'"
        for u in UserDemo.objects.raw(sql):
            cur_user = u
        if request.session['waf_flag'] is True:
            context = {'message_waf': 'The site is protected by WAF'}
            res_username = if_text_vulnerable_sql(user_name, request)
            res_user_password = if_text_vulnerable_sql(user_password, request)
            if res_username or res_user_password:
                messages.error(request, "sql injection!")
                return render(request, 'main/sql_demo.html', context)
        else:
            context = {'message_waf': 'The site is unprotected by WAF'}
        try:
            messages.success(request, 'You logged in as {}'.format(cur_user.username))
        except AttributeError:
            messages.error(request, "user not found")
        except Exception as e:
            print(e.__class__)
            return render(request, 'main/sql_demo.html', context)

        return render(request, 'main/sql_demo.html', context)


def homepage(request):
    return render(request, template_name='main/home.html')


@api_view(['POST'])
def sql_api(request):
    text = request.data.get('text')
    result = if_sql_text_vulnerable_without_saving_to_logger(text)
    json_response = {"sql prediction": result}
    return Response(json_response)

@api_view(['POST'])
def xss_api(request):
    text = request.data.get('text')
    result = if_xss_text_vulnerable_without_saving_to_logger(text)
    json_response = {"xss prediction": result}
    return Response(json_response)


def index(request):
    return render(request, 'form.html')


def stored_xss(request):
    try:
        if request.method == 'GET':
            from django.contrib.auth.models import User
            if request.session['waf_flag'] is True:
                all_users = list(User.objects.values())
                desired_keys = ["first_name", "last_name"]
                for user in all_users:
                    filtered_dict = {k: v for k, v in user.items() if k in desired_keys}
                    x = [k for k, v in filtered_dict.items() if
                         len(v) > 0 and if_text_vulnerable_xss_from_response(v, user['username'], request)]
                    for i in x:
                        user[i] = 'XSS ATTACK'
                return render(request, 'main/form.html', {'users': all_users,
                                                          'message_waf': 'The site is protected by WAF'})
            else:
                all_users = list(User.objects.values())
                return render(request, 'main/form.html', {'users': all_users,
                                                          'message_waf': 'The site is unprotected by WAF'})

    except Exception as e:
        print(e.__class__)
        return HttpResponse(e.__class__)


def xss_output(request):
    if request.method == 'GET':
        return render(request, template_name='main/xss_demo_output.html')


def demo_xss(request):
    if request.method == 'GET':
        if request.session['waf_flag'] is True:
            context = {'message_waf': 'The site is protected by WAF'}
        else:
            context = {'message_waf': 'The site is unprotected by WAF'}

        return render(request, 'main/xss_demo.html', context)

    if request.method == 'POST':
        search_id = request.POST.get('txtName')
        if request.session['waf_flag'] is True:
            if if_text_vulnerable(search_id, request) is True:
                context = {'text': "XSS ATTACK", 'message_waf': 'The site is protected by WAF'}
                template = loader.get_template('main/xss_demo_output.html')
                return HttpResponse(template.render(context, request))
            else:
                html = search_id
                context = {'text': html, 'message_waf': 'The site is protected by WAF'}
                return render(request, 'main/xss_demo_output.html', context)
        else:
            html = search_id
            context = {'text': html, 'message_waf': 'The site is unprotected by WAF'}
            return render(request, 'main/xss_demo_output.html', context)
