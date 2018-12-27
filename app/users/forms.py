from django import forms

from app.crawlers import auth
from app.utils.forms import ConfirmForm


class LoginForm(forms.Form):
    username = forms.CharField(label='北商學生資訊系統帳號')
    password = forms.CharField(label='北商學生資訊系統密碼',
                               widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        success, cookies = auth.login(username, password)

        if not success:
            raise forms.ValidationError('登入失敗')

        self.cleaned_data['cookies'] = cookies


class LogoutForm(ConfirmForm):
    check_label = '您確定要登出嗎？'
