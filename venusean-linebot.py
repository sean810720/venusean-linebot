'''
[LINEBot] 無敵小咪

- Heroku 網址:
https://venusean-linebot.herokuapp.com/callback
'''

# 共用
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser

# 爬蟲
import requests
from bs4 import BeautifulSoup
import json

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

    # 只回應 LINE 官方以外的帳號
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        result = ""

        # 台股指數
        if "大盤" in event.message.text or "台股" in event.message.text:

            # 大盤指數頁面
            res = requests.get(
                "https://histock.tw/%E5%8F%B0%E8%82%A1%E5%A4%A7%E7%9B%A4", verify=False)
            res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, "html.parser")

            # 抓出大盤指數
            stock_index = soup.select(".clr-rd")[0].text.strip()
            stock_updown = soup.select(".clr-rd")[1].text.strip()
            stock_rate = soup.select(".clr-rd")[2].text.strip()

            # 組出結果
            result = "目前台股大盤指數 {} \n漲跌 {} \n漲幅 {}".format(
                stock_index, stock_updown, stock_rate)

        # 美元匯率
        elif "美元" in event.message.text or "美金" in event.message.text:

            # 台銀匯率頁面
            res = requests.get(
                "https://rate.bot.com.tw/xrt?Lang=zh-TW", verify=False)
            res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, "html.parser")

            # 抓出美金匯率
            rate_buy = soup.select(".rate-content-sight")[4].text.strip()
            rate_sell = soup.select(".rate-content-sight")[3].text.strip()

            # 組出結果
            result = "目前美元匯率 \n買 {} \n賣 {}".format(rate_buy, rate_sell)

        # 日幣匯率
        elif "日元" in event.message.text or "日幣" in event.message.text:

            # 台銀匯率頁面
            res = requests.get(
                "https://rate.bot.com.tw/xrt?Lang=zh-TW", verify=False)
            res.encoding = 'utf8'
            soup = BeautifulSoup(res.text, "html.parser")

            # 抓出日幣匯率
            rate_buy = soup.select(".rate-content-sight")[18].text.strip()
            rate_sell = soup.select(".rate-content-sight")[17].text.strip()

            # 組出結果
            result = "目前日元匯率 \n買 {} \n賣 {}".format(rate_buy, rate_sell)

        # 疫情日報
        elif "疫情" in event.message.text:
            res = requests.get(
                "https://ghost-island-ab1d8-default-rtdb.firebaseio.com/covid-19/0.json", verify=False)
            res.encoding = 'utf8'
            jsons = json.loads(res.text)

            # 組出結果
            result = "最新本土疫情 \n確診 {} \n死亡 {}".format(
                jsons['new_confirmed'],
                jsons['new_deaths']
            )

        # 台電供電狀況
        elif "台電" in event.message.text or "電力" in event.message.text:
            res = requests.get(
                "https://ghost-island-ab1d8-default-rtdb.firebaseio.com/power/0.json", verify=False)
            res.encoding = 'utf8'
            jsons = json.loads(res.text)

            # 組出結果
            result = "目前台電狀況 \n{} ({}%)".format(
                jsons['power_status'],
                jsons['curr_util_rate']
            )

        # 目前新片
        elif "電影" in event.message.text or "新片" in event.message.text or "好片" in event.message.text:
            res = requests.get(
                "https://movieshowapp-3def6.firebaseio.com/MovieData.json", verify=False)
            res.encoding = 'utf8'
            jsons = json.loads(res.text)

            # 組出結果
            result = "目前有這幾部新片\n"
            count = 1
            for movie in jsons:
                if count <= 20:
                    if len(movie['imdb_rating']) > 0:
                        result += '\n{}. {} ({})'.format(count,
                                                         movie['title'],
                                                         movie['imdb_rating'])
                        count += 1
                else:
                    break

        # 聊天垃圾話
        elif event.message.text == '無敵小咪聊天':
            res = requests.post(
                "https://api.howtobullshit.me/bullshit", verify=False)
            res.encoding = 'utf8'

            # 組出結果
            result = res.text.replace('Bad Request', '')
            result = result.replace('&nbsp;', '').strip()

        # 打招呼
        elif "無敵小咪" in event.message.text:
            greetings = ['Hi', '幹嘛', '您好', '天氣不錯喔', '吃飽了嗎', '安安', '收到']

            # 組出結果
            result = greetings[
                random.randint(0, len(greetings))
            ]

        # 回應用戶
        if len(result) > 0:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result)
            )


# 主程式
if __name__ == "__main__":
    app.run()
