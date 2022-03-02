from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
import configparser
from app import routes, models_for_line

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
