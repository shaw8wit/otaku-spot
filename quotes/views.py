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

url = 'https://animechan.vercel.app/api/'


def index(request):
    """
    The default route function for Anime Quotes Application
    """

    # Authenticated users view their home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("quotes:allquotes", kwargs={'page': 1}))

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("quotes:register"))


def allquotes(request, page):
    """
    Returns all the quotes from the api.
    """

    if not request.session.has_key(str(page)):
        response = requests.get(f"{url}quotes?page={page}")
        d = response.json()
        request.session[str(page)] = d
    else:
        d = request.session[str(page)]
    return render(request, "quotes/index.html", {
        'data': d,
        'page': page,
        'l': [i for i in range(1, 11)]
    })


def login_view(request):
    """
    Logs user in if valid data is given else return a error message.
    """

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("quotes:index"))
        else:
            return render(request, "quotes/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "quotes/login.html")


def logout_view(request):
    """
    Logs user out.
    """

    logout(request)
    return HttpResponseRedirect(reverse("quotes:index"))


def register(request):
    """
    Registers the user if possible else returns an error message.
    """

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
        return HttpResponseRedirect(reverse("quotes:index"))
    else:
        return render(request, "quotes/register.html")


def search(request):
    """
    Renders the search page.
    """

    return render(request, "quotes/search.html")


def display(request, n):
    """
    Returns the data to be displayed on the random quotes link or from search.
    """

    try:
        if n == 0:
            response = requests.get(url + 'random')
            data = response.json()
        elif request.method == "POST":
            option = request.POST["option"]
            value = request.POST["value"]
            request.session['last'] = value
            if not request.session.has_key(value):
                field = 'title' if option == 'anime' else 'name'
                response = requests.get(
                    f'{url}quotes/{option}?{field}={value}')
                d = response.json()
                request.session[value] = d
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
    """
    Renders the about page.
    """

    return render(request, "quotes/about.html")


def contact(request):
    """
    Renders the contact page.
    """

    return render(request, "quotes/contact.html")


@csrf_exempt
def addData(request):
    """
    Adds or deletes saved quote data from users.
    """

    if request.method == "POST":
        content = json.loads(request.body)
        user = request.user
        if user.is_authenticated:
            try:
                anime = content['anime']
                character = content['character']
                quote = content['quote']
                addDel = content['addDel']
                if addDel:
                    if not Data.objects.filter(anime=anime, character=character, quote=quote).exists():
                        data = Data.objects.create(
                            anime=anime, character=character, quote=quote)
                        data.save()
                    else:
                        data = Data.objects.get(
                            anime=anime, character=character, quote=quote)
                    user.data.add(data)
                    user.save()
                    return HttpResponse(status=201)
                else:
                    data = Data.objects.get(
                        anime=anime, character=character, quote=quote)
                    user.data.remove(data)
                    user.save()
                    return HttpResponse(status=200)
            except Exception as e:
                return JsonResponse({
                    "error": f'{e} seems to be the problem'
                }, status=400)
        else:
            return JsonResponse({
                "error": "Login to save quotes."
            }, status=400)
    return JsonResponse({
        "error": "POST request required."
    }, status=400)


@csrf_exempt
@login_required
def profile(request):
    """
    Renders the profile page.
    Send PUT request to change userdata.
    """

    user = request.user
    if request.method == "PUT":
        try:
            content = json.loads(request.body)
            username = content['username']
            email = content['email']
            change = False
            if user.username != username:
                if User.objects.filter(username=username).exists():
                    return HttpResponse(status=204)
                change = True
                user.username = username
            if user.email != email:
                if User.objects.filter(email=email).exists():
                    return HttpResponse(status=204)
                change = True
                user.email = email
            if change:
                user.save()
                return HttpResponse(status=202)
            return HttpResponse(status=200)
        except:
            return JsonResponse({
                "error": "Something went wrong!!"
            }, status=400)

    return render(request, "quotes/profile.html", {
        'data': user.data.all(),
    })
