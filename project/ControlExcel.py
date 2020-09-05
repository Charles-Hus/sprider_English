# -*- coding:utf-8 -*-
"""
    @Author:ACheng
    @Date:2020/8/30
    @Content:
        操作Excel文件
        对Excel文件进行增删改查
"""
import xlrd  # 读取数据
import xlwt  # 写入数据
from xlutils.copy import copy

FILEPATH = r'..\src\SearchWord.xls'      # 存放单词的文件


class ControlExcel:

    def weather_the_word_exit_in_excel(self, word):
        """
        判断是否存在单词表中
        :param word: 用来判断的单词，看看数据表里有没有
        :return:{"flag": 记录是否存在于单词表中, "index": 记录单词索引}
        """
        print("ControlExcel().weather_the_word_exit_in_excel(word)",word)

        flag = False    # 记录是否存在于单词表中
        index = 0       # 记录单词索引

        excel_book = xlrd.open_workbook(FILEPATH)               # 获取excel文件
        sheet_content = excel_book.sheet_by_index(0)            # 通过索引获取表格
        cols_to_string = sheet_content.col_values(0)            # 获取第一列的内容

        for cols in cols_to_string:
            if cols == word:        # 在表中已经存在
                flag = True
                break
            index = index + 1       # 不在这一列，序号+1

        return_content = {"flag": flag, "index": index}
        return return_content

    def save_the_word_exit_in_excel(self, word_list):
        """
        存储单词
        :param word_list: 要存储的单词的列表
        :return:
        """
        print("ControlExcel().save_the_word_exit_in_excel(word_list)", word_list)

        data = xlrd.open_workbook(FILEPATH)         # 打开单词表文件
        new_workbook = copy(wb=data)                # 完成xlrd对象向xlwt对象转换
        excel_table = new_workbook.get_sheet(0)     # 获得要操作的页
        table = data.sheets()[0]                    # 获取第一个sheet表
        nrows = table.nrows                         # 获得行数,这个行数为存储元素的起点

        index_col = 0
        # if(word_list[0][1] | word_list[0][2]):
        if (word_list[1] or word_list[2]):
            #  有的单词匹配不到音标，这时候就把音标设置成" "
            # [单词，单词的音标，单词的意思，单词出现的次数默认为1]
            # word = [word_list[0][0],word_list[0][1]+word_list[0][2],word_list[1],"1"]
            word = [word_list[0], word_list[1] + word_list[2], word_list[3], "1"]
        else:
            # word = [word_list[0][0], " ", word_list[0][1], "1"]
            word = [word_list[0], " ", word_list[3], "1"]

        for value in word:
            excel_table.write(nrows, index_col, str(value))  # 因为单元格从0开始算，所以row不需要加一
            # 2020-8-31 历史错误Exception: Unexpected data type <class 'str'>, <class 'str'>  value --》str(value)

            index_col = index_col + 1

        new_workbook.save(FILEPATH)

    def tims_up_the_word_exit_in_excel(self, index_column):
        """
        更新出现的次数
        :param index_column: 单词的行数
        :return:
        """
        print("ControlExcel().tims_up_the_word_exit_in_excel(index_column)", index_column)
        data = xlrd.open_workbook(FILEPATH)
        new_workbook = copy(wb=data)
        excel_table = new_workbook.get_sheet(0)

        excel_book = xlrd.open_workbook(FILEPATH)
        sheet_content = excel_book.sheet_by_index(0)

        number = int(sheet_content.row_values(index_column)[3])+1
        excel_table.write(int(index_column), 3, "%s" % str(number))
        new_workbook.save(FILEPATH)

