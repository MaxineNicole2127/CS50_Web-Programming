from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponse
from django import forms
import random

from . import util

markdowner = Markdown()

def queryPresent(query):
    if query in util.list_entries():
        return True
    else:
        return False


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def results(request, tosearch):
    if queryPresent(tosearch):#tosearch in util.list_entries():
        raw_content = util.get_entry(tosearch)
        return render(request, "encyclopedia/results.html", {
            "content" : markdowner.convert(raw_content),
            "query" : tosearch,
            "exist": True
        })
    else:
        return render(request, "encyclopedia/results.html", {
            "query" : tosearch,
            "exist" : False
        })

def createNewPage(request):
    return render(request, "encyclopedia/newPage.html")


def randomPage(request):
    random_query = random.choice(util.list_entries())
    results = util.get_entry(random_query)

    return render(request, "encyclopedia/results.html", {
        "content" : markdowner.convert(results),
        "query" : random_query,
        "exist": True
    })


# class NewSearchForm(forms.Form):
#     query = forms.CharField(
#         label="", 
#         widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


# not working
def search(request):
    #FOUND SOLUTION: Create new object Form
    if request.method == "POST":
        query = request.POST['q']
        if queryPresent(query):
            results = util.get_entry(query)
            
            return render(request, "encyclopedia/trial.html", {
                'exists' : True,
                "content" : markdowner.convert(results),
                "query" : query
            })
        
        else:
            possible_matches = []
            for element in util.list_entries():
                if query in element:
                    possible_matches.append(element)
            return render(request, "encyclopedia/trial.html", {
                'exists' : False,
                "query" : query,
                "possible_matches": possible_matches,
                "possible_matches_length" : len(possible_matches)
            })