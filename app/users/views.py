from django.contrib import messages
from django.shortcuts import render, redirect

from app.crawlers.decorators import login_required, redirect_authenticated_user

from .forms import LoginForm, LogoutForm


SESSION_KEYS = ['cookies', 'std_id', 'std_name']


@redirect_authenticated_user
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        request.session['cookies'] = form.cleaned_data['cookies']
        request.session['std_id'] = username
        messages.success(request, '嗨，{} 歡迎使用'.format(username))
        return redirect('assessments:index')

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout(request):
    form = LogoutForm(request.POST or None)
    if form.is_valid() and form.cleaned_data['check']:
        for key in SESSION_KEYS:
            if key not in request.session:
                continue

            del request.session[key]

        messages.info(request, '感謝您的使用')
        return redirect('root')

    return render(request, 'users/logout.html', {'form': form})
