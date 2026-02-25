from django.shortcuts import render

# Create your views here.
def news_home(reguest):
    return render(reguest, "main/templates/page.html")

def index(request):
    return HttpResponse("<h4>Я рот ебал твой бля</h4>")

def about(request):
    return render(request, "main/page.html")