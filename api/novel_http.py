#!/usr/bin/env python
# -*- coding: utf-8 -*-
#小说接口http
from flask import Flask, jsonify, request
from flask_cors import CORS
from novel_api import Novel
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET'])
def test():
    return jsonify({'status':'True','message':'Hello world'})

@app.route('/search_novel', methods=['POST', 'GET'])
def search_novel():
    data = request.get_data()
    data = data.replace("'", '"')
    data = json.loads(data)
    novel_name = data.get('novel',None)
    if novel_name:
        obj = Novel()
        result = obj.get_novel(name=novel_name)
        return jsonify({'status':'True','message':'小说搜索成功','data':result})
    else:
        return jsonify({ 'status': 'False', 'message': '小说名称不能为空' })

@app.route('/get_novel_chapter', methods=['POST', 'GET'])
def get_novel_chapter():
    data = request.get_data()
    data = data.replace("'", '"')
    data = json.loads(data)
    novel_url = data.get('novel_url',None)
    sort_id = data.get('sort',None)
    if novel_url:
        obj = Novel()
        result = obj.get_chapter(url=novel_url,sort_id=sort_id)
        return jsonify({'status':'True','message':'小说章节获取成功','data':result})
    else:
        return jsonify({ 'status': 'False', 'message': '小说名称不能为空' }) 


@app.route('/get_novel_chapter_content', methods=['POST', 'GET'])
def get_novel_chapter_content():
    data = request.get_data()
    data = data.replace("'", '"')
    data = json.loads(data)
    chapter_url = data.get('chapter_url',None)
    if chapter_url:
        obj = Novel()
        result = obj.get_content(url=chapter_url)
        return jsonify({'status':'True','message':'小说内容获取成功','data':result})
    else:
        return jsonify({ 'status': 'False', 'message': '小说章节不能为空' })

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8090,debug=True)
