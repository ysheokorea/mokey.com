from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import NumberInput, TextInput

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='password 1', widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'비밀번호를 입력하세요'
        }))
    password2 = forms.CharField(label='password 2', widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'비밀번호를 확인해주세요'
        }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets={
            'username':forms.TextInput(attrs={
                'name':"username",
                'placeholder':"이름",
                'class':"form-control",
            }),
            'email':forms.EmailInput(attrs={
                'name':"email",
                'id':"emailAddress",
                'placeholder':"이메일",
                'class':"form-control",
            }),
        }


class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['email']
        widgets={
            'email':forms.EmailInput(attrs={
                'name':"email",
                'placeholder':"이메일",
                'class':"form-control",
            })
        }

class SetPasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='password 1', widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'비밀번호를 입력하세요'
        }))
    password2 = forms.CharField(label='password 2', widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'비밀번호를 확인해주세요'
        }))
    class Meta:
        model = User
        fields=['password1','password2']