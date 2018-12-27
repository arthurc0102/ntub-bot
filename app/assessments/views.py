from django.shortcuts import render

from app.crawlers.decorators import login_required


@login_required
def index(request):
    return render(request, 'assessments/index.html')
