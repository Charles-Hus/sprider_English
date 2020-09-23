# -*- config:utf-8 -*-
"""
    @Author:ACheng
    @Date:2020/8/31
    @Content:
        主方法

        1、读取写存放单词的txt文件
        2、操作入口
"""
import re
import sys
from time import sleep
from project.BaseWordFilter import BaseWordFilter
from project.RequestPage import RequestPage
from project.ControlExcel import ControlExcel


PATHREADFILE = r"..\src\test1.txt"
PATHWRITEFILE = r"..\src\listen_text.txt"

class MainFunction:

    def __init__(self):
        self.lists_of_a_line_word = []
        self.sentence = ""

    def read_data_in_txt(self):
        """
        读取test1.txt文件，并请求必应翻译页面，获取单词的意思
        :return:
        """
        print("MainFunction().read_data_in_txt()")
        with open(PATHREADFILE, "r", encoding='UTF-8') as file_of_me:
            while True:
                docuument_line = file_of_me.readline()          # 获取一行数据

                if not docuument_line:                          # 判断文件是否为空,若为空就停止运行
                    break
                else:                                           # 如果有数据，come on 干活
                    self.txt_word_get_meaning(docuument_line)
        file_of_me.close()

    def txt_word_get_meaning(self,docuument_line):
        """
        从read_data_in_txt中读取每一行txt文件的内容，把每一个单词的意思查出来
        :param docuument_line:
        :return:
        """
        print("MainFunction().txt_word_get_meaning(docuument_line)",docuument_line)

        a_line_word = docuument_line.replace("\n", "")          # 去掉换行符

        self.sentence = a_line_word
        # 示例参数值
        # sentence = 'This matter is too important to be left in the control of an inexpericnced

        a_line_words = re.findall(r'[a-zA-Z]+', a_line_word)    # 提取这一行的英文
        # 去掉数字 标点( . , ? ! [ ] " " - ( ) ) ===》 匹配 所有的英文

        for index_word in range(len(a_line_words)):
            # 是否在基础单词表中
            the_word_weather_exist = BaseWordFilter().weather_exit_in_base_word(a_line_words[index_word])
            the_word_weather_in_excel = ControlExcel().weather_the_word_exit_in_excel(a_line_words[index_word])

            if not(the_word_weather_exist) and not(the_word_weather_in_excel["flag"]):
                print("都不存在 开整吧")

                # 设置请求参数
                params = {
                    'q': '%s' % a_line_words[index_word],
                    'form': 'Z9LH5',
                    'sp': '-1',
                    'pq': '%s' % a_line_words[index_word],
                    'sk': '',
                }
                try:
                    response_html_text = RequestPage().request_page(params)  # 调用请求的方法

                except:
                    print(">>>>>>>>>> 2020-5-8 历史错误 HTTPSConnectionPool 没联网提示")
                    sys.exit()

                if RequestPage().match_word_meaning(response_html_text):
                    # ['This matter is too important to be left in the control of an inexpericnced',
                    #  [('this', '美 [ðɪs] ', '英 [ðɪs] '), ('pron.', '这；这里；这时；(前述二物中的)后者'), ('adj.', '这；即将来到的；今…'),
                    #   ('adv.', '这个；本；这样；这么')]]
                    self.lists_of_a_line_word.append(RequestPage().match_word_meaning(response_html_text))
                else:
                    continue
                sleep(1)  # 慢点，免得给我封印了

            elif not(the_word_weather_exist) and the_word_weather_in_excel["flag"]:
                print("不在基础单词表 but 在excel库种  times+1")
                try:
                    ControlExcel().tims_up_the_word_exit_in_excel(the_word_weather_in_excel["index"])  # 就是存在 就让time +1
                except PermissionError:
                    print(">>>>>>>>>> [Errno 13] Permission denied: '..\\src\\SearchWord.xls'"
                          "2020-8-31 历史错误：要先关闭文件SearchWord.xls")
                    sys.exit()

            elif the_word_weather_exist:
                print("在基础单词表中  pass")

        self.writ_word_in_txt_excel()

    def writ_word_in_txt_excel(self):
        """
        将单词写入文件 listen_text
        :return:
        """
        print("MainFunction().writ_word_in_txt_excel()", self.lists_of_a_line_word)
        write_file = open(PATHWRITEFILE, "a", encoding='utf-8')
        write_file.write("============================================================\n")
        write_file.write(self.sentence + "\n")
        counter = 0

        while counter < len(self.lists_of_a_line_word):
            # self.lists_of_a_line_word[counter] 示例参数值
            # [('creature', "美 ['kritʃər] ", "英 ['kriːtʃə(r)] "), ('n.', '生物；东西；创造物；〈美〉牛马')]
            get_weather = ControlExcel().weather_the_word_exit_in_excel(self.lists_of_a_line_word[counter][0])

            if not get_weather["flag"]:

                for content in self.lists_of_a_line_word[counter]:

                    for index in content:
                        # 2020-8-31 历史错误： ('abbr.', '女的；女性的；阴性的；（演奏或歌唱）强') tupe类型——》str类型
                        # 但是需要保证 单词，音标不会被强转成单个字符s	e	l	f
                        try:
                            write_file.write("%s" % index)
                        except TypeError:
                            print(index)
                            for item in index:
                                write_file.write("%s" % item)
                            write_file.write("\n")
                    write_file.write("\n")

                write_file.write("\n")
                try:
                    # print(self.lists_of_a_line_word[counter])
                    ControlExcel().save_the_word_exit_in_excel(self.lists_of_a_line_word[counter])
                except PermissionError:
                    print(">>>>>>>>>>> [Errno 13] Permission denied: '..\\src\\SearchWord.xls'"
                          "2020-8-31 历史错误：要先关闭文件SearchWord.xls")
                    sys.exit()
            else:
                try:
                    ControlExcel().tims_up_the_word_exit_in_excel(get_weather["index"])      # 就是存在 就让time +1
                except PermissionError:
                    print(">>>>>>>>>> [Errno 13] Permission denied: '..\\src\\SearchWord.xls'"
                          "2020-8-31 历史错误：要先关闭文件SearchWord.xls")
                    sys.exit()

            counter += 1
        sleep(1)
        write_file.close()


if __name__ == '__main__':
    MainFunction().read_data_in_txt()
    print("╔==============================╗\n"
          "│                              │ \n"
          "│        Author：aCheng        │ \n"
          "│   单词都整出来后，记得要背下来 │ \n"
          "│                              │ \n"
          "╚≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡╝\n")
