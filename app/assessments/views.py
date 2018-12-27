from django.contrib import messages
from django.shortcuts import render, redirect

from app.crawlers.assessment import get_assessments
from app.crawlers.decorators import login_required

from . import services
from .forms import FillForm


@login_required
def index(request):
    assessments = get_assessments(request.session['cookies'])

    if assessments is None:
        messages.info(request, '目前不是教學評量填寫時間')
        return redirect('root')

    return render(request, 'assessments/index.html', {
        'assessments': assessments,
    })


@login_required
def fill(request, class_no):
    cookies = request.session['cookies']
    assessment = services.get_assessment(cookies, class_no)
    if not assessment:
        messages.warning(request, '本課程編號不存在')
        return redirect('assessments:index')

    if not assessment['params']:
        messages.info(request, '本教學評量已經填寫過了')
        return redirect('assessments:index')

    form = FillForm(request.POST or None)
    if form.is_valid():
        score = form.cleaned_data['score']
        suggestions = form.cleaned_data['suggestions']
        result = services.fill(cookies, assessment, score, suggestions)
        if result:
            messages.success(request, '填寫完成')
        else:
            messages.error(request, '填寫失敗，請重試或聯絡系統管理員')

        return redirect('assessments:index')

    return render(request, 'assessments/fill.html', {'form': form})


@login_required
def fill_all(request):
    cookies = request.session['cookies']
    assessments = get_assessments(cookies)
    form = FillForm(request.POST or None)

    if form.is_valid():
        score = form.cleaned_data['score']
        suggestions = form.cleaned_data['suggestions']
        result = services.fill_all(cookies, assessments, score, suggestions)
        if result:
            messages.success(request, '填寫完成')
        else:
            messages.error(request, '填寫失敗，請重試或聯絡系統管理員')

        return redirect('assessments:index')

    return render(request, 'assessments/fill.html', {'form': form})
