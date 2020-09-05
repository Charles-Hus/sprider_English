# -*-coding:utf-8-*-
"""
    @Author:ACheng
    @Date:2020/8/29
    @Content:
       生成基础单词过滤表，一般都是在单词积累到一定程度，很多单词都背过了，
       这个时候把会的单词放入..\src\baseWord.txt中，运行此方法，生成基础单词过滤表
"""

def produce_word_filter_table(self):

    import re

    """
    生成基础单词过滤表,基础单词库文件 转换成 基础单词表
    :return:
    """
    base_word_file = open(r"..\src\baseWord.txt", "r", encoding='UTF-8')
    base_word_text = base_word_file.read()

    #  97对应a 123对应z
    for i in range(97, 123):
        # 遍历 a-z 分别匹配出相应首字母的单词
        word = re.findall(r'(\b%s.*?) ' % chr(i), base_word_text)
        writefile = open(r"..\src\baseWordAlphabet\%s.txt" % chr(i), "a", encoding='utf-8')
        # 将单词加入到基础单词表中
        writefile.write(str(word))
        writefile.close()

    base_word_file.close()