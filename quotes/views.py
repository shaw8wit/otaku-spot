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


def display(request, r):
    return render(request, "quotes/display.html", {
        'value': "random" if r == 0 else "from search"
    })
