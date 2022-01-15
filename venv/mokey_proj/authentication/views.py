from django.contrib.auth.forms import UserCreationForm
from django.http.request import validate_host
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, ResetPasswordForm, SetPasswordForm
from django.contrib.auth.models import User
import traceback

import json

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.core.mail import EmailMessage, message

import threading

# Create your views here.

def user_login(request):
    """
    # 목적 : 로그인 기능
    """
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, '회원정보를 다시 확인해주세요')

    return render(request, 'authentication/login.html')

def user_register(request):
    """
    # 목적 : 회원가입 기능
    """
    form = CreateUserForm()

    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']        
    
        if not User.objects.filter(username=email).exists():
            try:
                user=User.objects.create_user(username=email, first_name=username)
                user.set_password(password)
                user.save()
                messages.success(request, username+' 님 회원가입을 축하드립니다')
                return redirect('authentication:user_login')
            except:
                messages.warning(request, '계정정보를 다시 확인해주세요')
                return redirect('authentication:user_register')
        else:
            messages.warning(request, '이미 존재하는 이메일입니다')
            return redirect('authentication:user_register')            

    context={'form':form}
    return render(request, 'authentication/register.html', context)


def naver_user_register(request):
    """
    # 목적 : 네이버 ID를 이용한 로그인 구현
    """
    form = CreateUserForm()
    if request.method=="GET":
        context={'form':form}
        return render(request, 'authentication/register_naver.html', context)
    if request.method=="POST":
        email=json.loads(request.body).get('email')
        username=json.loads(request.body).get('name')
        
        try:
            if User.objects.filter(username=email).exists():
                user = authenticate(request, username=email)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.warning(request, '계정정보를 다시 확인해주세요')
            else:
                try:
                    user=User.objects.create_user(username=email, first_name=username)
                    # user.set_password(password)
                    user.save()
                    messages.success(request, username+' 님 회원가입을 축하드립니다')
                    return redirect('authentication:user_login')
                except:
                    messages.warning(request, '계정정보를 다시 확인해주세요')
                    return redirect('authentication:user_register')
        except:
            print(traceback.format_exc())
        return JsonResponse('complete', safe=False)

def user_logout(request):
    """
    # 목적 : 로그아웃
    """
    logout(request)
    return redirect('authentication:user_login')

class EmailThread(threading.Thread):
    """
    # 목적 : Email Threading!
    """
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)


def resetPassword(request):
    """
    # 목적 : 패스워드 재설정 email 발송
    """

    form=ResetPasswordForm()
    if request.method=="GET":
        context={
            'form':form,
        }
        return render(request, 'authentication/reset-password.html', context)
    
    if request.method=="POST":
        context={
            'form':form,
        }
        try:
            email=request.POST['email']
        
            user = User.objects.filter(username=email)
            current_site=get_current_site(request)
            email_contents={
                'user':user[0],
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user[0].first_name)),
                'token':PasswordResetTokenGenerator().make_token(user[0]),
            }

            if user.exists():
                link=reverse('authentication:setPassword', kwargs={'uidb64' : email_contents['uid'], 'token' : email_contents['token']})

            email_subject='[Mokey] 비밀번호 재설정 인증메일'
            reset_url = 'http://'+current_site.domain+link
            email_body = \
                user[0].first_name +'님 안녕하세요\n\n'+ \
                '빅데이터 기반 키워드 분석 모키 Mokey입니다.\n' + \
                '요청하신 비밀번호 재설정 메일을 확인해주시기 바랍니다.\n' + \
                '아래의 링크를 클릭하시면 비밀번호 재설정 화면으로 이동합니다.\n' +\
                reset_url
            email = EmailMessage(
                # Email Subject
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email]
            )
            EmailThread(email).start()
            messages.success(request, '인증메일 발송이 완료되었습니다.')        
            return render(request, 'authentication/reset-password.html', context)

        except:
            messages.warning(request, '[Error] 다시 시도 해주세요')        
            print(traceback.format_exc())
            return render(request, 'authentication/reset-password.html', context)
            
    context={
        'form':form,
    }
    return render(request, 'authentication/reset-password.html', context)

def setPassword(request, uidb64, token):
    """
    # 목적 : 패스워드 재설정
    """
    form=SetPasswordForm()
    if request.method=="GET":
        try:
            user_name = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(first_name=user_name)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, '인증메일이 만료되었습니다. 인증요청 다시 해주세요')
                return render(request, 'authentication/reset-password.html')
        except Exception as e:
            pass


        context={
            'form':form,
            'uidb64':uidb64,
            'token':token,
        }
        return render(request, 'authentication/set-password.html', context)

    if request.method=="POST":
        context={
            'form':form,
            'uidb64' : uidb64,
            'token' : token,
        }
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, '비밀번호가 일치하지 않습니다')
            return render(request, 'authentication/set-password.html', context)

        if len(password1) < 6:
            messages.error(request, '비밀번호가 너무 짧습니다')
            return render(request, 'authentication/set-password.html', context)        

        try:
            user_name = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(first_name=user_name)           
            user.set_password(password2)
            user.save()

            messages.success(request, '비밀번호 재설정이 완료되었습니다')
            return redirect('authentication:user_login')
        except Exception as e:
            messages.info(request, '[Error] 다시 시도 해주세요')
            return render(request, 'authentication/set-password.html', context)  