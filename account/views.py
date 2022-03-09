from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import Account
#from .forms import SignUpForm


def start(request):
    return render(request, 'account/start.html', {})


def login(request):
    return render(request, 'account/login.html', {})


def register(request):
    if request.method == 'POST':
        data = RegisterForm(request.POST)
        if data.is_valid():
            account = data.save(commit=False)
            account.save()
            return redirect('start')
    else:
        data = RegisterForm()
    return render(request, 'account/register.html', {'form': data})


def mypage(request):
    return render(request, "account/mypage.html", {})
