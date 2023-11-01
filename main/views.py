from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import random
import json


# Create your views here.
def index(request):
    now = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    return HttpResponse(f"<h1>現在時刻:{now}</h1>")


def get_books(request):
    mybook = {1: "java_book", 2: "python_book", 3: "c_book"}

    return HttpResponse(json.dumps(mybook))


def get_lottory2(request):
    lottorynum = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    lottorynum_str = " ".join(map(str, lottorynum))
    return render(request, "lottory.html", {"x": x, "lottorynum": lottorynum_str})


def get_lottory(request):
    lottorynum = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    lottorynum_str = " ".join(map(str, lottorynum)) + f" 特別號:{x}"
    return HttpResponse("<h1>本期預測號碼:</h1>" + "<h2>" + lottorynum_str + "</h2>")
