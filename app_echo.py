'''
[LINEBot] 無敵小咪

- Heroku 網址:
https://venusean-linebot.herokuapp.com/
'''


from inspect import signature
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
app = Flask(__name__)


# 設定
line_bot_api = LineBotApi(
    'Dn3vefwx2MFm7rcB5z7J3psYODNV0VBAkr0szrkh8nv4pWBgBJnQEAvqZf571SXBRawH4HBMerUsob9mtewsBUY7Cf1N6EOk5hdSFGUp7A1ayr6KsuBFKQr9ieRW8gkHabCS4aIaAnBjBV6yKB64vwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d29f1d6448804ab36ba42486f335d950')


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

        if event.message.text == "大盤指數":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前大盤指數萬八上看兩萬")
            )
        elif event.message.text == "美元匯率":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前美元匯率 28.01")
            )
        elif event.message.text == "小咪" or event.message.text == "無敵小咪":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="你好")
            )
        else:
            pass


# 主程式
if __name__ == "__main__":
    app.run()
