from collections import Counter, namedtuple

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
    skills_count = dict(Counter([repo['language'] for repo in repos]))
    Skill = namedtuple('Skill', "name level font_name")

    if skills_count.get(None):
        del skills_count[None]

    icon_replacements ={
        "CSS": "css3",
        "Shell": "linux",
        "Makefile": "linux",
        "HTML": "html5",
        "Puppet": "ruby",
        "Scala": "java",
        "VimL": "linux",
        "Haskell": "linux",
        "Clojure": "linux",
        "Elixir": "linux"
    }
    unsorted_skills = [
        Skill(name=skill[0], level=skill[1], font_name=icon_replacements.get(skill[0], skill[0]))
        for skill
        in skills_count.items()
    ]
    skills = sorted(unsorted_skills, key=lambda s: s.level, reverse=True)
    if len(skills) > 8:
        skills = skills[:8]
    elif len(skills) > 4:
        skills = skills[:4]

    gists = github.users(username).gists.get()
    return render(request, 'index.html', locals())
