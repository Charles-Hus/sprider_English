# -*- config:utf-8 -*-
"""
    @Author:ACheng
    @Date:2020/8/30
    @Content:
        请求页面，并做相应的数据处理

        1、匹配单词
        2、处理单词
"""
import re
import requests


class RequestPage:
    def request_page(self, params):
        """
        用来请求必应的翻译引擎
        :param params:
        :return:
        """
        print("RequestPage().request_page()")

        url = "https://cn.bing.com/dict/search?"            # 请求必应翻译
        response_html = requests.get(url, params)           # 获取返回的必应翻译的页面html代码
        response_html_text = response_html.text             # 将html 代码转换成文本格式
        return response_html_text

    def match_word_meaning(self, text):
        """
        对请求返回的页面进行分析,
        :param text: 要翻译的整个句子
        :return: 对应单词的音标以及内容的列表
        """
        print("RequestPage().match_word_meaning()")

        phonetic_symbol_rule = r'<div class="hd_area">.*?<div class="hd_div" id="headword"><h1><strong>' \
                               r'(.*?)</strong></h1></div>.*?<div class="hd_prUS b_primtxt">' \
                               r'(.*?)</div>.*?<div class="hd_pr b_primtxt">' \
                               r'(.*?)</div>.*?<ul>'
        word_meaning_rule = r'<li><span class="pos">' \
                            r'(.*?)</span><span class="def b_regtxt"><span>' \
                            r'(.*?)</span></span></li>'

        word_meaning_compare = re.compile(word_meaning_rule, re.S)
        word_meaning_compare_list = re.findall(word_meaning_compare, text)

        # 首先这个单词的意思能匹配出来，如果匹配，有音标又如何
        if word_meaning_compare_list:

            phonetic_symbol_campare = re.compile(phonetic_symbol_rule, re.S)
            phonetic_symbol_campare_list = re.findall(phonetic_symbol_campare, text)
            if phonetic_symbol_campare_list:

                phonetic_symbol_of_english = self.phonetic_symbol(phonetic_symbol_campare_list[0][2])  # 英式音标
                phonetic_symbol_of_american = self.phonetic_symbol(phonetic_symbol_campare_list[0][1])  # 美式音标
                try:
                    meaning_of_word_list = [phonetic_symbol_campare_list[0][0],
                                            phonetic_symbol_of_english,
                                            phonetic_symbol_of_american,
                                            word_meaning_compare_list
                                            ]
                    print("meaning_of_word_list:",meaning_of_word_list)
                    return meaning_of_word_list
                except IndexError:
                    print(">>>>>>>>>> 2020-5-8 历史错误："
                          "1、页面结构更换，正则匹配规则需要更改 定位（ phoneticSymbol()方法）\n "
                          "2、单词有误看下单词是不是错了")
                    return None
        else:
            print("RequestPage().match_word_meaning() word_meaning_compare_list",word_meaning_compare_list)
            return None

    '''**************************************************************************************************
    # [('n.', '前景；观点；人生观；世界观'), ('v.', '瞪着看；瞧；以目光压倒(对方)；比…好看')]
    # phonetic_symbolCampareList          [('Outlook', "美&#160;['aʊt.lʊk] ", "英&#160;['aʊt.lʊk] ")]
    # phonetic_symbolCampareList[0]       ('Outlook', "美&#160;['aʊt.lʊk] ", "英&#160;['aʊt.lʊk] ")
    # phonetic_symbolCampareList[0][0]    Outlook
    # phonetic_symbolCampareList[0][1]    "美&#160;['aʊt.lʊk] "
    # phonetic_symbolCampareList[0][2]    "英&#160;['aʊt.lʊk] "
    **************************************************************************************************'''

    def phonetic_symbol(self,value_of_list):
       """
       匹配音标，音标格式化
       但由于网页解析的原因，我们看到的音标实标上是一堆Unicode编码代表的
            这个时候就need
                                     ——————格式化音标

       DICT是一个存放常量Unicode与音标的显示码的数组
       :param valueOfList:
       :return: 
       """
       print("RequestPage().phonetic_symbol(value_of_list)",value_of_list)

       # 音标所对应的值
       DICT = {"230": "æ", "240": 'ð', '331': 'ŋ', '593': 'ɑ', '594': 'ɒ', '596': 'ɔ',
               '601': 'ə', '603': 'ɛ', '604': 'ɜ', '609': 'ɡ', '618': 'ɪ',
               '643': 'ʃ', '650': 'ʊ', '652': 'ʌ', '658': 'ʒ', '712': 'ˈ', '716': 'ˌ',
               '720': 'ː', '952': 'θ', "160": " "}

       try:
           if value_of_list:
               phonetic_symbol = value_of_list

               comp = re.compile(r"&#(.*?);")       # 将音标中的十六进制转换成符号英&#160
               phonetic_symbol_replice_string = re.findall(comp, phonetic_symbol)

               # 在这里把&#160;更换成" "
               length_of_phonetic_symbol_replice_string = len(phonetic_symbol_replice_string)

               if length_of_phonetic_symbol_replice_string:

                   for i in range(length_of_phonetic_symbol_replice_string):
                       phonetic_symbol = phonetic_symbol.replace("&#%s;" % phonetic_symbol_replice_string[i],
                                                                 DICT[phonetic_symbol_replice_string[i]])
               return phonetic_symbol

       except IndexError:
           print(">>>>>>>>>> IndexError 2020-5-4 历史错误：没有匹配到音标")
           return ""





