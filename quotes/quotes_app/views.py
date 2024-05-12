from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import QuoteForm, AuthorForm, RegisterForm, LoginForm
from .models import Quote, Author, User


def main(request):
    quotes = Quote.objects.all()
    context = {'quotes': quotes}
    return render(request, 'base.html', context)


def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'quote.html', {'form': form})

    return render(request, 'quote.html', {'form': QuoteForm()})


def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'author.html', {'form': form})

    return render(request, 'author.html', {'form': AuthorForm()})


def author_detail(request, fullname):
    quotes_by_author = Quote.objects.filter(author=fullname)

    author = Author.objects.get(fullname=fullname)

    context = {'author': author, 'quotes_by_author': quotes_by_author}
    return render(request, 'author_detail.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes_app:main')
        else:
            return render(request, 'register.html', context={"form": form})

    return render(request, 'register.html', context={"form": RegisterForm()})


def user_login(request):
    if request.user.is_authenticated:
        return redirect(to='quotes_app:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='quotes_app:login')

        login(request, user)
        return redirect(to='quotes_app:main')

    return render(request, 'login.html', context={"form": LoginForm()})


@login_required
def user_logout(request):
    logout(request)
    return redirect(to='quotes_app:main')
