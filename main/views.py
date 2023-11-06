from django.shortcuts import render
from datetime import datetime
import random
import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

from linebot import LineBotApi, WebhookHandler, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


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
