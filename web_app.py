#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web界面版本的中英翻译和英文字典系统
使用Flask框架提供Web服务
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from translator import ChineseEnglishTranslator

app = Flask(__name__)
CORS(app)

# 全局翻译器实例
translator = None

def init_translator():
    """初始化翻译器"""
    global translator
    try:
        translator = ChineseEnglishTranslator()
        return True
    except Exception as e:
        print(f"翻译器初始化失败: {e}")
        return False

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    """翻译API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'zh')
        
        if not text:
            return jsonify({'error': '请输入要翻译的文本'})
        
        if not translator:
            return jsonify({'error': '翻译器未初始化'})
        
        if source_lang == 'zh':
            result = translator.translate_chinese_to_english(text)
        else:
            result = translator.translate_english_to_chinese(text)
        
        return jsonify({
            'success': True,
            'original_text': text,
            'translation': result,
            'source_lang': source_lang
        })
        
    except Exception as e:
        return jsonify({'error': f'翻译失败: {str(e)}'})

@app.route('/api/translate_with_examples', methods=['POST'])
def translate_with_examples():
    """翻译并获取例句API"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        source_lang = data.get('source_lang', 'zh')
        
        if not text:
            return jsonify({'error': '请输入要翻译的文本'})
        
        if not translator:
            return jsonify({'error': '翻译器未初始化'})
        
        result = translator.translate_with_examples(text, source_lang)
        
        return jsonify({
            'success': True,
            **result
        })
        
    except Exception as e:
        return jsonify({'error': f'翻译失败: {str(e)}'})

@app.route('/api/dictionary/<word>')
def dictionary(word):
    """字典查询API"""
    try:
        if not translator:
            return jsonify({'error': '翻译器未初始化'})
        
        word_info = translator.get_word_definition(word)
        
        if word_info:
            return jsonify({
                'success': True,
                'word': word,
                **word_info
            })
        else:
            return jsonify({'error': f'未找到单词 "{word}" 的定义'})
        
    except Exception as e:
        return jsonify({'error': f'查询失败: {str(e)}'})

@app.route('/api/health')
def health():
    """健康检查API"""
    return jsonify({
        'status': 'healthy',
        'translator_ready': translator is not None
    })

if __name__ == '__main__':
    # 创建templates目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # 初始化翻译器
    print("正在初始化翻译器...")
    if init_translator():
        print("翻译器初始化成功!")
        print("启动Web服务器...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("翻译器初始化失败，无法启动Web服务")