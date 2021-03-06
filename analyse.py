#coding:utf-8
import re
import sys

class Analyse:
	def transform(self,s,d):
		if s in d:
			return True,s
		elif s[-2:] == "ed":
			if s[:-1] in d:
				return True,s[:-1]
			elif s[:-2] in d:
				return True,s[:-2]
			else:
				return False,s
		elif s[-3:] == "ing":
			if s[:-3] in d:
				return True,s[:-3]
			elif s[:-3] + "e" in d:
				return True,s[:-3] + "e"
			else:
				return False,s
		elif s[-1:] == "s":
			if s[:-1] in d:
				return True,s[:-1]
			else:
				return False,s
		elif s[-2:] == "es":
			if s[:-2] in d:
				return True,s[:-2]
			else:
				return False,s
		else:
			return False,s

	def get_word(self,text):
		r = re.compile("[a-zA-Z]+")
		l = r.findall(text)
		return l

	def load_black_file(self,black_file_name):
		word_dic = {}
		if black_file_name:
			text = open(black_file_name).read()
			word_list = self.get_word(text)
			for word in word_list:
				word_dic[word.strip().lower()] = -1
		return word_dic
	def load_word(self,in_file_name,word_dic):
		text = open(in_file_name).read()
		word_list = self.get_word(text)
		for word in word_list:
			if len(word) < 2:
				continue
			word = word.lower()
			if word in word_dic:
				if word_dic[word] > 0:
					word_dic[word] += 1
				else:
					word_dic[word] -= 1
			else:
				word_dic[word] = 1
			# isin,word = self.transform(word,word_dic)
			# if isin:
			# 	if word_dic[word] != -1:
			# 		word_dic[word] += 1
			# else:
			# 	word_dic[word] = 1
		
		return len(word_list)
	def cal_count(self,word_dic):
		outside_num = 0
		set_num = 0
		for word in word_dic:
			if word_dic[word] > 0:
				set_num += 1
			elif word_dic[word] < -1:
				outside_num += 1
		return outside_num,set_num
	def write_word(self,out_file_name,word_dic,range_min,range_max):
		result = open(out_file_name,"w")
		range_min = range_min if range_min >= 0  else 0
		write_num = 0
		if range_max == '$':
			for word in word_dic:
				if word_dic[word] >= range_min:
					write_num += 1
					result.write(word + "<")
					for space in xrange(40 - len(word)):
						result.write("-")
					result.write(">" + str(word_dic[word]) + "\n")
		else:
			for word in word_dic:
				if word_dic[word] < int(range_max) and word_dic[word] >= range_min:
					write_num += 1
					result.write(word + "<")
					for space in xrange(40 - len(word)):
						result.write("-")
					result.write(">" + str(word_dic[word]) + "\n")
		result.close()
		return write_num
	def start(self,in_file_name,out_file_name,black_file_name,range_min,range_max):
		word_dic = self.load_black_file(black_file_name)
		black_num = len(word_dic)
		sum_num = self.load_word(in_file_name,word_dic)
		outside_num,set_num = self.cal_count(word_dic)
		write_num = self.write_word(out_file_name,word_dic,range_min,range_max)
		print u"文件总单词数:",sum_num
		print u"黑名单单词数:",black_num
		print u"去重后在黑名单中的单词数:",outside_num
		print u"去重后不在黑名单的单词数:",set_num
		print u"符合要求词频的单词数:",write_num

def main():
	a = Analyse()
	if len(sys.argv) > 4:
		a.start(sys.argv[1],sys.argv[2],"black_word.txt",int(sys.argv[3]),sys.argv[4])
	else:
		print 
		print u"请按如下方法使用:"
		print u"    analyse.py [待分析的文本名] [要输出的文件名] [最小词频] [最大词频]"
		print u"    如果不要求有最大词频，那么将其设置为 $ "
		print 
		print u"黑名单文件默认为 black_word.txt,该文件必须存在，不需要设置黑名单的话置其内容为空即可"
		print u"若需设置黑名单,则每行为一个单词，出现在黑名单中的单词将不会出现在最终结果中"

if __name__ == "__main__":
	main()
