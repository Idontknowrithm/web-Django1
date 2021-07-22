from django import forms
from .models import User
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages = {
            'required' : '아이디를 입력해주세요.'
        },
        max_length = 20, label = '사용자 이름')
    password = forms.CharField(
        error_messages = {
            'required' : '비밀번호를 입력해주세요.'
        },
        widget = forms.PasswordInput, label = '비밀번호')
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                self.add_error('username', '아이디를 확인해주세요.')
                return
            user = User.objects.get(username = username)
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호를 확인해주세요.')
            else:
                self.user_id = user.id
