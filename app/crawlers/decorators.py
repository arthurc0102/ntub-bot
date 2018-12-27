from django.contrib import messages
from django.shortcuts import redirect

from .auth import check_login


def login_required(view_func):
    def check(request, *args, **kwargs):
        cookies = request.session.get('cookies')
        if cookies and check_login(cookies):
            return view_func(request, *args, **kwargs)

        messages.info(request, '您尚未登入')
        return redirect('users:login')
    return check


def redirect_authenticated_user(view_func):
    def check(request, *args, **kwargs):
        cookies = request.session.get('cookies')
        if cookies and check_login(cookies):
            msg = '{} 您已經登入'.format(request.session.get('std_id', ''))
            messages.info(request, msg)
            return redirect('root')

        return view_func(request, *args, **kwargs)
    return check
