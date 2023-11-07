from django.shortcuts import render
from django.http import JsonResponse
from . import forms, models

def form_view(request):
    form = forms.CommentForm()

    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            print("valid")
            cd = form.cleaned_data
            uc = models.UserComments(
                first_name = cd["first_name"],
                last_name = cd["last_name"],
                comment = cd["comment"],
            )
            uc.save()
            return JsonResponse({
                "message": "success"
            })
    
    return render(request, "blog.html", {"form": form})