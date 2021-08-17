from DBwaf.logger import save_attack_to_logger
from connectionWithDockerModel.main import xss_proccesor, predict_sqli_attack


def if_text_vulnerable(text, request):
    res = xss_proccesor(text)
    cur_email = request.user.get_username()

    if res > float(request.session['threshold_xss']):
        save_attack_to_logger(cur_email, res, text, type_attack='XSS')
        return True
    else:
        return False


def if_text_vulnerable_sql(text, request):
    res = predict_sqli_attack(text)
    cur_email = request.user.get_username()
    if res > float(request.session['threshold_sql']):
        save_attack_to_logger(cur_email, res, text, 'SQL INJECTION')
        return True
    else:
        return False


def if_text_vulnerable_xss_from_response(text, username, request):
    res = xss_proccesor(str(text))
    cur_email = username
    session_threshold_xss_ = request.session['threshold_xss']

    if res > float(session_threshold_xss_):
        save_attack_to_logger(cur_email, res, text, "Stored XSS")
        return True
    else:
        return False
