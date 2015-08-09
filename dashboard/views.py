from collections import Counter, namedtuple

from django.shortcuts import render
from requests import get
import tortilla


from django.shortcuts import render_to_response


def with_template(template):
    """
    A decorator to render the view with a template. The view just
    returns a contect dictionary. eg:

    @with_template('index.html')
    def index_view(request):
        return {"name": "dave"}

    Source: https://gist.github.com/0atman/1912bfd62f8dbd93cfa5
    """
    def template_decorator(view):
        def view_wrapper(*args, **kwargs):
            return render_to_response(
                template,
                view(*args, **kwargs)
            )
        return view_wrapper
    return template_decorator


@with_template('index.html')
def dashboard(request, username):
    github = tortilla.wrap('https://api.github.com', cache_lifetime=60)
    github_user = github.users.get(username)
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
        "Elixir": "linux",
        "Arduino": "linux"
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
    return locals()
