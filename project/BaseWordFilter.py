# -*- config:utf-8 -*-
"""
    @Author:ACheng
    @Date:2020/8/30
    @Content:
        基础单词过滤功能，取出那些超级超级简单的单词

        1、判断一个单词是否为一个基础单词
        2、生成基础单词过滤表
"""
import re


class BaseWordFilter:
    def weather_exit_in_base_word(self, word):
        """
        判断一个单词是否为一个基础单词
        :param word:   要判断的单词
        :return: boolean 类型
                 true：属于基础单词
                 false：不属于基础单词
        """

        file_path = r"..\src\baseWordAlphabet\%s.txt" % str(list(word)[0]).lower()  # 文件路径，过滤文件名为单词首字母.txt
        base_word_file = open(file_path, "r", encoding='UTF-8')                     # 打开文件
        base_word = base_word_file.read()                                           # 读取文件
        weather_or_not_exit = re.findall(r"'%s '" % word, base_word)                # 匹配文件是否在基础单词库中

        if weather_or_not_exit:                                                     # 存在
            return True
        else:                                                                       # 不存在
            return False

