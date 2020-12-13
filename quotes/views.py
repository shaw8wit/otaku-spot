from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import User, Data

import requests
import json

url = 'https://animechanapi.xyz/api/quotes/'


def index(request):

    # Authenticated users view their home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("allquotes", kwargs={'page': 1}))

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("register"))


def allquotes(request, page):
    if not request.session.has_key(str(page)):
        response = requests.get(url + f"?page={page}")
        d = response.json()
        d = d['data']
        request.session[str(page)] = d
        print(f"\n\nfetching page {page}\n\n")
    else:
        d = request.session[str(page)]
    return render(request, "quotes/index.html", {
        'data': d,
        'page': page,
        'l': [i for i in range(1, 11)]
    })


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
    Returns the data to be displayed on the random quotes link or from search.
    """

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
                response = requests.get(url + f'?{option}={value}')
                d = response.json()
                request.session[value] = d['data']
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


def contact(request):
    return render(request, "quotes/contact.html")


@csrf_exempt
def addData(request):
    if request.method == "POST":
        content = json.loads(request.body)
        if request.user.is_authenticated:
            anime = content['anime']
            character = content['character']
            quote = content['quote']
            try:
                data = Data.objects.get(
                    anime=anime, character=character, quote=quote)
                request.user.data.remove(data)
            except Data.DoesNotExist:
                data = Data.objects.create(
                    anime=anime, character=character, quote=quote)
                data.save()
                request.user.data.add(data)
            request.user.save()
            return HttpResponse(status=204)
        else:
            return JsonResponse({
                "error": "Login to save quotes."
            }, status=400)
        return HttpResponse(status=204)
    return JsonResponse({
        "error": "POST request required."
    }, status=400)


@login_required
def profile(request):
    return render(request, "quotes/profile.html", {
        'data': request.user.data.all(),
    })
