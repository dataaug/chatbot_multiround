import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from chat import Generator

# 需要在不同目录import
import sys

app = Flask(__name__)
CORS(app, resources=r'/*')


engine = Generator()
sents = []

@app.route("/", methods=["GET", 'POST'])
def hello_world():
    if request.method == 'POST':
        print('文本生成暂不支持图片和视频请求')
        return

    else:  # GET方法 代表是关键词请求
        key_word = request.args.get("key_word")
        industry = request.args.get("industry")
        global sents
        sents.append(key_word)
        print('当前对话:', sents)
        res = engine.generate(sents)
        if '[CLS]' in res[0] or key_word.lower() == 'exit': #机器人结束对话或者出现结束代码
            res = ['无言以对......请开始下一个话题']
            with open('chat_saved.txt', 'a', encoding='utf-8') as fw:
                fw.write('[SEP]'.join(sents) + '\n')
            sents = []
        else:
            sents.append(res[0])
            print(res)

        return jsonify(list_of_data=res)

