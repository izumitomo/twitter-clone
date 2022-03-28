from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import Account


def start(request):
    return render(request, 'account/start.html', {})


def login(request):
    return render(request, 'account/login.html', {})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.save()
            return redirect('start')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})


def mypage(request):
    return render(request, "account/mypage.html", {})
