==========================================
				README
==========================================
文件路径：
	"..\src\test1.txt"          存放要翻译的单词
	"..\src\listen_text.txt"    存放翻译后的单词
	"..\src\SearchWord.xls"     excel数据库,存放历史查找记录
	"project/MainFunction.py"   主方法

*******************************************	
需要的第三方库：
	name{

		time
		sys
		re
		xlrd
		xlwt
		xlutils
		requests
	}
	
	安装方法：
		pip install {{ name }}
*******************************************

使用步骤：
	1、把要翻译的单词放在..\src\test1.txt里面
	2、打开主方法project/MainFunction.py
	3、开始翻译单词，生成的单词会存放到..\src\SearchWord.xls & ..\src\listen_text.txt
	4、重复单词不会存储，只会在..\src\SearchWord.xls的 出现次数times 中+1

