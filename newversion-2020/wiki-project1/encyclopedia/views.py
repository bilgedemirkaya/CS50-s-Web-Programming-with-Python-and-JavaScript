from django.shortcuts import render,redirect
from django import forms

from . import util
import markdown2
from markdown2 import Markdown
import random

class Searching(forms.Form):
    search = forms.CharField(label="Search")
class EditedPost(forms.Form):
    content = forms.CharField(label="content",widget=forms.Textarea)


def index(request):

    if request.method == "POST":
        search = Searching(request.POST)
        if search.is_valid():
            answer = search.cleaned_data["search"]
            contents = util.get_entry(answer)
            if contents != None:
                return render(request, "encyclopedia/content.html",{
                    "contents":contents,"title":answer})
            else:
                all_entries = util.list_entries()
                entries = []
                for entry in all_entries:
                    if answer in entry:
                        entries.append(entry)
                if entries == []:
                    message= "There is no match with the query. You can create one"
                    return render(request,"encyclopedia/error.html",{"message": message})
                else:
                    return render(request, "encyclopedia/index.html", {
                        "entries": entries})

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,title):
    if request.method == "POST":
        title = request.POST['title']
        edited_content = request.POST['edited']
        markdowner = Markdown()
        content = markdowner.convert(edited_content)
        util.save_entry(title,content)
        return render(request,"encyclopedia/content.html",{"title":title,"content":content})
    contents = util.get_entry(title)
    if contents != None:
        return render(request,"encyclopedia/content.html",{
            "content":contents, "title":title })
    else:
        message="There is no such a page, please go back"
        return render(request,"encyclopedia/error.html",{"message": message})

def newentry(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['newpage']
        markdowner = Markdown()
        content = markdowner.convert(content)

        all_entries = util.list_entries()
        for entry in all_entries:
            if title == entry:
                message="Sorry, There is already a content with the same title"
                return render(request,"encyclopedia/error.html",{"message": message})
        util.save_entry(title,content)
        return render(request,"encyclopedia/content.html",{"title":title,"content":content})
    else:
        return render(request,"encyclopedia/newentry.html")

def edit(request,title):
    if request.method == "POST":
        content = EditedPost(request.POST)
        if content.is_valid():
            edited = content.cleaned_data["content"]
            util.save_entry(title, edited)
            return redirect('/' + title)
        else:
            message = "Can't be edited"
            return render(request, "encyclopedia/error.html", {"message": message})
    else:
        content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
            "title": title,"content":content, "form": EditedPost()})
def randomed(request):
    all_entries = util.list_entries()
    entry = random.choice(all_entries)
    content = util.get_entry(entry)
    return render(request,"encyclopedia/content.html", {"title":entry,"content":content})
