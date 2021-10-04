import re
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from main.models import Logger

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
PASSWORD_RULES = 'The password must contain: alphabets between [a-z], At least one alphabet of Upper Case [A-Z], ' \
                 'At least 1 number or digit between [0-9], At least 1 special character. '


def check_strong_password(password: object) -> object:
    # Primary conditions for password validation :
        # Minimum 8 characters.
        # The alphabets must be between [a-z]
        # At least one alphabet should be of Upper Case [A-Z]
        # At least 1 number or digit between [0-9].
        # At least 1 special character

    if len(password) >= 8:
        if not re.search("[a-z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[@_!#$%^&*()<>?/\|}{~:]", password):
            return False
        elif re.search("\s", password):
            return False
        else:
            return True  # Valid Password
    else:
        return False


def validation_email(email: str) -> bool:
    if re.search(regex, email):
        return True
    else:
        return False


def authenticate_user(email: str, password: str):
    return authenticate(username=email, password=password)


@csrf_exempt
def change_password_anno(request):
    @csrf_protect
    def change_password_protected():
        if request.method == 'GET':
            return render(request, template_name='main/change_password.html')

        elif request.method == 'POST':
            new_pss = request.POST.get('new_pass')
            if check_strong_password(new_pss) is False:
                messages.error(request, PASSWORD_RULES)
                return redirect('change_pass')
            else:
                u = User.objects.get(username=cache.get('user'))
                u.set_password(new_pss)
                u.save()
                messages.success(request, "Password changed! login again with the new password")
                cur_email = cache.get('user')
                l1 = Logger(email=cur_email, threshold=0, command='CSRF attack attempt', type_attack='CSRF', if_warn=True,
                            date=datetime.now())
                l1.save()
                cache.delete('user')
                logout(request)
                return render(request, template_name='main/home.html')

    if request.session['waf_flag'] is True:
        return change_password_protected(request)

    else:
        return change_password(request)


def change_password(request):
    if request.method == 'GET':
        return render(request, template_name='main/change_password.html')

    elif request.method == 'POST':
        new_pss = request.POST.get('new_pass')
        if check_strong_password(new_pss) is False:
            messages.error(request, PASSWORD_RULES)
            return redirect('change_pass')
        else:
            u = User.objects.get(username=cache.get('user'))
            u.set_password(new_pss)
            u.save()
            messages.success(request, "Password changed! login again with the new password")
            logout(request)
            cache.delete('user')
            return render(request, template_name='main/home.html')


def login_page(request):
    if request.method == 'GET':
            if cache.get('user') is None:
                return render(request, template_name='main/login.html')
            else: return render(request, template_name='main/home.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if validation_email(email) is False:
            messages.error(request, 'email must be in the format of example@example.com')
            return redirect('login')

        elif check_strong_password(password) is False:
            messages.error(request, PASSWORD_RULES)
            return redirect('login')

        cache.set('user', authenticate_user(email,password))
        if cache.get('user') is not None:

            login(request, cache.get('user'))
            messages.success(request, f'You are logged in as {cache.get("user")}')
            return redirect('home')

        else:
            messages.error(request, 'The combination of the user name and the password is wrong!')
            return redirect('login')

@login_required(login_url='/login/')
def logoutpage(request):
    logout(request)
    cache.delete('user')
    messages.success(request, f'You have been logged out!')
    return render(request, template_name='main/home.html')