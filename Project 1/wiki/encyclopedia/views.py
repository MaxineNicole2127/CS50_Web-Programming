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

'''

class NewPageForm(forms.Form):
    title = forms.CharField(
        label = "",
        widget = forms.TextInput(attrs={'placeholder': 'Title', 
                                      'style' : 'padding: 7px 15px; border: 1px solid #DFE1E5; border-radius: 4px; outline: none;'})
    )

'''

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


from django.urls import reverse
from django.http import HttpResponseRedirect

# not working
def search(request):
    #FOUND SOLUTION: Create new object Form
    if request.method == "POST":
        query = request.POST['q']
        if queryPresent(query):
            return HttpResponseRedirect(reverse("encyclopedia:results", args = (query,)))
        else:
            possible_matches = []
            for element in util.list_entries():
                if query in element:
                    possible_matches.append(element)
            return render(request, "encyclopedia/noresult.html", {
                'exists' : False,
                "query" : query,
                "possible_matches": possible_matches,
                "possible_matches_length" : len(possible_matches)
            })

def edit(request):
    if request.method == "POST":
        query = request.POST.get("query")
        results = util.get_entry(query)
        return render(request, "encyclopedia/editPage.html", {
            "query": query,
            "content" : results
        })
    
def saveChangeInPage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("encyclopedia:results", args = (title,)))

def saveNewContent(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if queryPresent(title):
            return render(request, "encyclopedia/newPage.html", {
                "error": True,
                "title" : title,
                "content" : content
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:results", args = (title,)))
        
    return render(request, "encyclopedia/newPage.html", {
        "error": False,
        "title" : "",
        "content" : ""
    })