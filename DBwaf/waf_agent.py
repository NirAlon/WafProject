from datetime import datetime

from main.models import Logger
from connectionWithDockerModel.main import xss_proccesor, predict_sqli_attack


def if_text_vulnerable(text, request):
    res = xss_proccesor(text)

    cur_email = request.user.get_username()

    if res > float(request.session['threshold_xss']):
        l1 = Logger(email=cur_email, threshold=res, command=text, type_attack='Reflected XSS', if_warn=True,
                    date=datetime.now())
        l1.save()
        return True
    else:
        return False


def if_text_vulnerable_sql(text: str, request):
    res = predict_sqli_attack(text)
    cur_email = request.user.get_username()
    if res > float(request.session['threshold_sql']):
        l1 = Logger(email=cur_email, threshold=res, command=text, type_attack='SQL', if_warn=True,
                    date=datetime.now())
        l1.save()
        return True
    else:
        return False


def if_text_vulnerable_xss_from_response(text, username, request):
    res = xss_proccesor(str(text))
    cur_email = username
    session_threshold_xss_ = request.session['threshold_xss']

    if res > float(session_threshold_xss_):
        l1 = Logger(email=cur_email, threshold=res, command=text, type_attack='Stored XSS', if_warn=True,
                    date=datetime.now())
        l1.save()
        return True
    else:
        return False
