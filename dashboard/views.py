from collections import Counter

from django.shortcuts import render
from requests import get
import tortilla


def dashboard(request, username):
    auth_token = "d8e50e1990c4ab6d50015e0f36c2db865bf5c5bf"
    github = tortilla.wrap('https://api.github.com', cache_lifetime=5)
    github.config.headers.Authorization = "token " + auth_token

    github_user = github.users.get(username)
    "https://api.stackexchange.com/2.2/users/333294?site=stackoverflow"
    repos =  github.users(username).repos.get()
    skills = Counter([repo['language'] for repo in repos])

    return render(request, 'index.html', locals())
