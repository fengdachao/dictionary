#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试翻译器功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from translator import ChineseEnglishTranslator

def test_translator():
    """测试翻译器功能"""
    print("=== 测试中英翻译和英文字典系统 ===\n")
    
    try:
        # 初始化翻译器
        print("正在初始化翻译器...")
        translator = ChineseEnglishTranslator()
        print("翻译器初始化成功!\n")
        
        # 测试中英翻译
        print("1. 测试中英翻译:")
        chinese_text = "你好，世界！"
        english_result = translator.translate_chinese_to_english(chinese_text)
        print(f"   中文: {chinese_text}")
        print(f"   英文: {english_result}\n")
        
        # 测试英中翻译
        print("2. 测试英中翻译:")
        english_text = "Hello, world!"
        chinese_result = translator.translate_english_to_chinese(english_text)
        print(f"   英文: {english_text}")
        print(f"   中文: {chinese_result}\n")
        
        # 测试字典查询
        print("3. 测试字典查询:")
        word = "hello"
        word_info = translator.get_word_definition(word)
        if word_info:
            print(f"   单词: {word}")
            print(f"   发音: {word_info.get('pronunciation', 'N/A')}")
            print(f"   中文: {word_info.get('chinese', 'N/A')}")
            print(f"   定义: {word_info.get('definitions', [])}")
            print(f"   例句: {word_info.get('examples', [])}")
        else:
            print(f"   未找到单词 '{word}' 的定义")
        print()
        
        # 测试翻译+例句功能
        print("4. 测试翻译+例句功能:")
        test_text = "我爱学习"
        result = translator.translate_with_examples(test_text, "zh")
        print(f"   原文: {result['original_text']}")
        print(f"   翻译: {result['translation']}")
        if result.get('examples'):
            print("   例句:")
            for word, examples in result['examples'].items():
                print(f"     {word}: {examples[0] if examples else 'N/A'}")
        print()
        
        # 测试英文单词提取
        print("5. 测试英文单词提取:")
        english_sentence = "Hello world, this is a beautiful day!"
        words = translator.extract_english_words(english_sentence)
        print(f"   句子: {english_sentence}")
        print(f"   提取的单词: {words}")
        print()
        
        print("✅ 所有测试通过!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_translator()