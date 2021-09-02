import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import DBwaf.Serializers as Serializers

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


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_get_logger(request):
    if request.method == 'GET':
        log = Logger.objects.all()
        serializer = Serializers.LoggerSerializer(log, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = Serializers.LoggerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
