#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中英翻译和英文字典系统使用示例
"""

from translator import ChineseEnglishTranslator

def main():
    """使用示例"""
    print("=== 中英翻译和英文字典系统使用示例 ===\n")
    
    # 初始化翻译器
    translator = ChineseEnglishTranslator()
    
    # 示例1: 基础翻译
    print("示例1: 基础中英翻译")
    chinese_text = "今天天气很好，我想去公园散步。"
    english_result = translator.translate_chinese_to_english(chinese_text)
    print(f"中文: {chinese_text}")
    print(f"英文: {english_result}\n")
    
    # 示例2: 英中翻译
    print("示例2: 英中翻译")
    english_text = "I love learning new languages and exploring different cultures."
    chinese_result = translator.translate_english_to_chinese(english_text)
    print(f"英文: {english_text}")
    print(f"中文: {chinese_result}\n")
    
    # 示例3: 字典查询
    print("示例3: 英文字典查询")
    word = "beautiful"
    word_info = translator.get_word_definition(word)
    if word_info:
        print(f"单词: {word}")
        print(f"发音: {word_info['pronunciation']}")
        print(f"中文: {word_info['chinese']}")
        print("定义:")
        for i, definition in enumerate(word_info['definitions'], 1):
            print(f"  {i}. {definition}")
        print("例句:")
        for i, example in enumerate(word_info['examples'], 1):
            print(f"  {i}. {example}")
    print()
    
    # 示例4: 翻译+例句
    print("示例4: 翻译并显示例句")
    text = "学习英语很有趣"
    result = translator.translate_with_examples(text, "zh")
    print(f"原文: {result['original_text']}")
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
    
    print("\n=== 示例完成 ===")

if __name__ == "__main__":
    main()