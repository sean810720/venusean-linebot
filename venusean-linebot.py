'''
[LINEBot] 無敵小咪

- Heroku 網址:
https://venusean-linebot.herokuapp.com/callback
'''


from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser

# 爬蟲
import requests
from bs4 import BeautifulSoup

# 聊天垃圾話
import random

app = Flask(__name__)


# 基本設定
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get(
    'venusean-linebot',
    'channel_access_token'
))

handler = WebhookHandler(config.get(
    'venusean-linebot',
    'channel_secret'
))


# 接收平台來的通知
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 回應區
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        # 美元匯率
        if event.message.text == "美元匯率":

            # 台銀匯率頁面
            res = requests.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")
            res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, "html.parser")

            # 抓出美元匯率
            usd_rate = soup.select(".rate-content-sight")[4].text.strip()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前美元匯率 {}".format(usd_rate))
            )

        # 聊天垃圾話
        elif "小咪" in event.message.text:
            trash_talks = ['幹嘛', '您好', '今天天氣不錯喔', '吃飽了嗎', '早安']
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=trash_talks[
                        random.randint(0, len(trash_talks))
                    ]
                )
            )
        else:
            pass


# 主程式
if __name__ == "__main__":
    app.run()
