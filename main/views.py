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
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.META["HTTP_X_LINE_SIGNATURE"]
        body = request.body.decode("utf-8")
        try:
            events = parse.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event, MessageEvent):
                message = event.message.text
                message_object = None

                if message == "你好":
                    message_object = TextSendMessage(text="你也好!")
                elif message == "樂透":
                    message_object = TextSendMessage(text=get_lottory_num())
                elif "捷運" in message:
                    if "台北" in message:
                        url = "https://kuopoting.github.io/k1/assets/20200119_zh.png"
                    elif "台中" in message:
                        url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/taichung/20201112_zh.png?v=2"
                    elif "高雄" in message:
                        url = "https://assets.piliapp.com/s3pxy/mrt_taiwan/kaohsiung/202210_zh.png"
                    message_object = ImageSendMessage(
                        original_content_url=url, preview_image_url=url
                    )
                else:
                    reply_message = "我不懂你的意思"
                    message_object = TextSendMessage(text=reply_message)

                # if event.message.text=='hello':
                line_bot_api.reply_message(
                    event.reply_token,
                    # TextSendMessage(text='hello world')
                    message_object,
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


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


def get_lottory_num():
    lottorynum = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    lottorynum_str = " ".join(map(str, lottorynum))
    return lottorynum_str


def get_lottory(request):
    lottorynum = sorted(random.sample(range(1, 50), 6))
    x = random.randint(1, 50)
    lottorynum_str = " ".join(map(str, lottorynum)) + f" 特別號:{x}"
    return HttpResponse("<h1>本期預測號碼:</h1>" + "<h2>" + lottorynum_str + "</h2>")
