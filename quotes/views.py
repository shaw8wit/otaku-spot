from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout

from .models import User

import requests


def index(request):

    # Authenticated users view their home page
    if request.user.is_authenticated:
        return render(request, "quotes/index.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("register"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "quotes/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "quotes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quotes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            return render(request, "quotes/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "quotes/register.html")


def search(request):
    return render(request, "quotes/search.html")


def display(request, n):
    """
    Returns the data to be displayed on the random quotes link or from search
    """

    url = 'https://animechanapi.xyz/api/quotes/'
    try:
        if n == 0:
            response = requests.get(url + 'random')
            d = response.json()
            data = d['data'][0]
        elif request.method == "POST":
            option = request.POST["option"]
            value = request.POST["value"]
            request.session['last'] = value
            if not request.session.has_key(value):
                url += f'?{option}={value}'
                response = requests.get(url)
                d = response.json()
                request.session[value] = d['data']
                print(f'\n\nloaded once\n\n')
        if n != 0:
            d = request.session[request.session['last']]
            data = d[n % 10]
    except:
        data = {'quote': "Couldn't find what you were looking for",
                'character': "Shouvit Pradhan", 'anime': "Something went wrong"}

    return render(request, "quotes/display.html", {
        'quote': data['quote'],
        'character': data['character'],
        'anime': data['anime'],
        'n': n,
    })


def about(request):
    return render(request, "quotes/about.html")
