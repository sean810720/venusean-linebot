from app import line_bot_api, handler
from linebot.models import MessageEvent, TextMessage, TextSendMessage


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
                TextSendMessage(text="幹嘛")
            )
        else:
            pass
