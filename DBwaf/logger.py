import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from main.models import Logger


def logger_page(request):
    current_email = request.user.get_username()
    if request.method == 'GET':
        loggers = Logger.objects.filter(email=current_email)
        return render(request, template_name='main/logger.html', context={'loggers': loggers})

    if request.method == 'POST':
        select_attack_type = request.POST.get('radio')
        select = request.POST.get('if_alerted')

        if select == 'on':
            loggers1 = Logger.objects.filter(email=current_email, if_warn=True)
        else:
            loggers1 = Logger.objects.filter(email=current_email)

        if select_attack_type == 'sqli':
            loggers1_sql = loggers1.filter(type_attack='SQL')
            return render(request, template_name='main/logger.html', context={'loggers': loggers1_sql})
        elif select_attack_type == 'xss':
            loggers1_xss = loggers1.filter(
                Q(type_attack='Reflected XSS') | Q(type_attack='Stored XSS') | Q(type_attack='Dom XSS'))
            return render(request, template_name='main/logger.html', context={'loggers': loggers1_xss})
        elif select_attack_type == 'csrf':
            loggers1_csrf = loggers1.filter(type_attack='CSRF')
            return render(request, template_name='main/logger.html', context={'loggers': loggers1_csrf})

        return render(request, template_name='main/logger.html', context={'loggers': loggers1})


def export_logger_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="logger.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Date', 'Threshold', 'Type Attack', 'Command', 'If Warn'])

    logg = Logger.objects.all().values_list('email', 'date', 'threshold', 'type_attack', 'command', 'if_warn')
    for log in logg:
        writer.writerow(log)

    return response

def save_attack_to_logger(cur_email, res, text, type_attack):
    Logger.objects.create(
        email=cur_email, date=datetime.now(), threshold=res * 100,
        type_attack=type_attack, command=text, if_warn=True)
