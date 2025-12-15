from django.shortcuts import render

def gugudan_view(request, num):
    result = [f"{num} x {i} = {num*i}" for i in range(1, 10)]
    return render(request, "gugudan/gugudan.html", {"num": num, "result": result})
