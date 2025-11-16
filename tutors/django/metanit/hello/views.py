from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def about(request, name, age):
    return HttpResponse(f"""
            <h2>О пользователе</h2>
            <p>Имя: {name}</p>
            <p>Возраст: {age}</p>
    """)