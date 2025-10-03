#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开源翻译模型实现中英翻译和英文字典功能
支持翻译和英文例句查询
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re
import json
import os
from typing import List, Dict, Optional, Tuple


class ChineseEnglishTranslator:
    """中英翻译器类"""
    
    def __init__(self):
        """初始化翻译器"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {self.device}")
        
        # 初始化翻译模型
        self._init_translation_models()
        
        # 初始化字典数据
        self._init_dictionary()
    
    def _init_translation_models(self):
        """初始化翻译模型"""
        try:
            # 使用Helsinki-NLP的OPUS-MT模型进行中英翻译
            model_name_zh_en = "Helsinki-NLP/opus-mt-zh-en"
            model_name_en_zh = "Helsinki-NLP/opus-mt-en-zh"
            
            print("正在加载中英翻译模型...")
            self.zh_en_translator = pipeline(
                "translation", 
                model=model_name_zh_en, 
                device=0 if self.device == "cuda" else -1
            )
            
            print("正在加载英中翻译模型...")
            self.en_zh_translator = pipeline(
                "translation", 
                model=model_name_en_zh, 
                device=0 if self.device == "cuda" else -1
            )
            
            print("翻译模型加载完成!")
            
        except Exception as e:
            print(f"模型加载失败: {e}")
            print("尝试使用备用模型...")
            self._load_fallback_models()
    
    def _load_fallback_models(self):
        """加载备用翻译模型"""
        try:
            # 备用模型
            fallback_model = "t5-small"
            self.zh_en_translator = pipeline(
                "translation", 
                model=fallback_model, 
                device=0 if self.device == "cuda" else -1
            )
            self.en_zh_translator = self.zh_en_translator
            print("备用模型加载完成!")
        except Exception as e:
            print(f"备用模型也加载失败: {e}")
            raise
    
    def _init_dictionary(self):
        """初始化英文字典数据"""
        self.dictionary = {
            "hello": {
                "pronunciation": "/həˈloʊ/",
                "definitions": [
                    "used as a greeting or to begin a phone conversation",
                    "an expression of surprise or interest"
                ],
                "examples": [
                    "Hello, how are you today?",
                    "Hello! What a pleasant surprise!",
                    "Hello, this is John speaking."
                ],
                "chinese": "你好；哈喽"
            },
            "world": {
                "pronunciation": "/wɜːrld/",
                "definitions": [
                    "the earth, together with all of its countries and peoples",
                    "a particular region or group of countries"
                ],
                "examples": [
                    "The world is a beautiful place.",
                    "She traveled around the world.",
                    "The world of technology is rapidly changing."
                ],
                "chinese": "世界；地球"
            },
            "beautiful": {
                "pronunciation": "/ˈbjuːtɪfl/",
                "definitions": [
                    "pleasing the senses or mind aesthetically",
                    "of a very high standard; excellent"
                ],
                "examples": [
                    "The sunset was beautiful tonight.",
                    "She has a beautiful voice.",
                    "What a beautiful day it is!"
                ],
                "chinese": "美丽的；漂亮的"
            },
            "computer": {
                "pronunciation": "/kəmˈpjuːtər/",
                "definitions": [
                    "an electronic device for storing and processing data",
                    "a person who makes calculations"
                ],
                "examples": [
                    "I use my computer for work every day.",
                    "The computer crashed and I lost all my files.",
                    "Modern computers are very powerful."
                ],
                "chinese": "计算机；电脑"
            },
            "learn": {
                "pronunciation": "/lɜːrn/",
                "definitions": [
                    "gain or acquire knowledge of or skill in something",
                    "become aware of something"
                ],
                "examples": [
                    "Children learn quickly.",
                    "I want to learn how to cook.",
                    "We learn from our mistakes."
                ],
                "chinese": "学习；学会"
            },
            "love": {
                "pronunciation": "/lʌv/",
                "definitions": [
                    "an intense feeling of deep affection",
                    "a great interest and pleasure in something"
                ],
                "examples": [
                    "I love my family very much.",
                    "She loves reading books.",
                    "Love is the most powerful emotion."
                ],
                "chinese": "爱；喜欢"
            },
            "time": {
                "pronunciation": "/taɪm/",
                "definitions": [
                    "the indefinite continued progress of existence",
                    "a point of time as measured in hours and minutes"
                ],
                "examples": [
                    "Time flies when you're having fun.",
                    "What time is it now?",
                    "I don't have time for this."
                ],
                "chinese": "时间；时候"
            },
            "good": {
                "pronunciation": "/ɡʊd/",
                "definitions": [
                    "to be desired or approved of",
                    "having the required qualities"
                ],
                "examples": [
                    "That's a good idea.",
                    "She is a good student.",
                    "Have a good day!"
                ],
                "chinese": "好的；优秀的"
            },
            "friend": {
                "pronunciation": "/frend/",
                "definitions": [
                    "a person whom one knows and with whom one has a bond of mutual affection",
                    "a person who supports a cause or organization"
                ],
                "examples": [
                    "She is my best friend.",
                    "A friend in need is a friend indeed.",
                    "I made many friends at school."
                ],
                "chinese": "朋友；友人"
            },
            "home": {
                "pronunciation": "/hoʊm/",
                "definitions": [
                    "the place where one lives permanently",
                    "the place where something originates"
                ],
                "examples": [
                    "There's no place like home.",
                    "I'm going home now.",
                    "Home is where the heart is."
                ],
                "chinese": "家；家庭"
            }
        }
    
    def translate_chinese_to_english(self, chinese_text: str) -> str:
        """中文翻译为英文"""
        try:
            if not chinese_text.strip():
                return ""
            
            # 使用翻译模型进行翻译
            result = self.zh_en_translator(chinese_text)
            english_text = result[0]['translation_text']
            
            return english_text.strip()
        except Exception as e:
            print(f"翻译错误: {e}")
            return f"翻译失败: {e}"
    
    def translate_english_to_chinese(self, english_text: str) -> str:
        """英文翻译为中文"""
        try:
            if not english_text.strip():
                return ""
            
            # 使用翻译模型进行翻译
            result = self.en_zh_translator(english_text)
            chinese_text = result[0]['translation_text']
            
            return chinese_text.strip()
        except Exception as e:
            print(f"翻译错误: {e}")
            return f"翻译失败: {e}"
    
    def get_word_definition(self, word: str) -> Optional[Dict]:
        """获取单词定义和例句"""
        word_lower = word.lower().strip()
        return self.dictionary.get(word_lower)
    
    def extract_english_words(self, text: str) -> List[str]:
        """从文本中提取英文单词"""
        # 使用正则表达式提取英文单词
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        # 过滤掉太短的单词
        words = [word.lower() for word in words if len(word) > 2]
        return list(set(words))  # 去重
    
    def get_examples_for_text(self, text: str) -> Dict[str, List[str]]:
        """获取文本中单词的例句"""
        words = self.extract_english_words(text)
        examples = {}
        
        for word in words:
            word_info = self.get_word_definition(word)
            if word_info and 'examples' in word_info:
                examples[word] = word_info['examples']
        
        return examples
    
    def translate_with_examples(self, text: str, source_lang: str = "zh") -> Dict:
        """翻译并获取例句"""
        result = {
            "original_text": text,
            "translation": "",
            "examples": {},
            "word_definitions": {}
        }
        
        try:
            if source_lang == "zh":
                # 中文翻译为英文
                english_text = self.translate_chinese_to_english(text)
                result["translation"] = english_text
                
                # 获取英文例句
                examples = self.get_examples_for_text(english_text)
                result["examples"] = examples
                
                # 获取单词定义
                words = self.extract_english_words(english_text)
                for word in words:
                    word_info = self.get_word_definition(word)
                    if word_info:
                        result["word_definitions"][word] = word_info
                        
            else:
                # 英文翻译为中文
                chinese_text = self.translate_english_to_chinese(text)
                result["translation"] = chinese_text
                
                # 获取英文例句（从原文）
                examples = self.get_examples_for_text(text)
                result["examples"] = examples
                
                # 获取单词定义
                words = self.extract_english_words(text)
                for word in words:
                    word_info = self.get_word_definition(word)
                    if word_info:
                        result["word_definitions"][word] = word_info
            
            return result
            
        except Exception as e:
            result["error"] = str(e)
            return result


def main():
    """主函数 - 命令行界面"""
    print("=== 中英翻译和英文字典系统 ===")
    print("支持功能:")
    print("1. 中英翻译")
    print("2. 英中翻译") 
    print("3. 英文字典查询")
    print("4. 翻译并显示例句")
    print("输入 'quit' 退出程序")
    print("-" * 40)
    
    # 初始化翻译器
    try:
        translator = ChineseEnglishTranslator()
    except Exception as e:
        print(f"初始化失败: {e}")
        return
    
    while True:
        try:
            print("\n请选择功能:")
            print("1. 中英翻译")
            print("2. 英中翻译")
            print("3. 英文字典查询")
            print("4. 翻译并显示例句")
            print("5. 退出")
            
            choice = input("\n请输入选择 (1-5): ").strip()
            
            if choice == "1":
                text = input("请输入中文: ").strip()
                if text:
                    result = translator.translate_chinese_to_english(text)
                    print(f"翻译结果: {result}")
                    
            elif choice == "2":
                text = input("请输入英文: ").strip()
                if text:
                    result = translator.translate_english_to_chinese(text)
                    print(f"翻译结果: {result}")
                    
            elif choice == "3":
                word = input("请输入英文单词: ").strip()
                if word:
                    word_info = translator.get_word_definition(word)
                    if word_info:
                        print(f"\n单词: {word}")
                        print(f"发音: {word_info.get('pronunciation', 'N/A')}")
                        print(f"中文: {word_info.get('chinese', 'N/A')}")
                        print("定义:")
                        for i, definition in enumerate(word_info.get('definitions', []), 1):
                            print(f"  {i}. {definition}")
                        print("例句:")
                        for i, example in enumerate(word_info.get('examples', []), 1):
                            print(f"  {i}. {example}")
                    else:
                        print(f"未找到单词 '{word}' 的定义")
                        
            elif choice == "4":
                text = input("请输入要翻译的文本: ").strip()
                if text:
                    # 自动检测语言
                    if re.search(r'[\u4e00-\u9fff]', text):
                        source_lang = "zh"
                        print("检测到中文，将翻译为英文...")
                    else:
                        source_lang = "en"
                        print("检测到英文，将翻译为中文...")
                    
                    result = translator.translate_with_examples(text, source_lang)
                    
                    print(f"\n原文: {result['original_text']}")
                    print(f"翻译: {result['translation']}")
                    
                    if result.get('examples'):
                        print("\n相关例句:")
                        for word, examples in result['examples'].items():
                            print(f"\n{word}:")
                            for example in examples[:2]:  # 显示前2个例句
                                print(f"  • {example}")
                    
                    if result.get('word_definitions'):
                        print("\n单词释义:")
                        for word, info in result['word_definitions'].items():
                            print(f"\n{word}: {info.get('chinese', 'N/A')}")
                            if info.get('pronunciation'):
                                print(f"  发音: {info['pronunciation']}")
                            
            elif choice == "5":
                print("感谢使用，再见!")
                break
                
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()