
def firstUpower(str):
	return str[0].capitalize() + str[1:].lower()

def firstUpowerOnly(str):
	return str[0].upper() + str[1:]
	
def convert(one_string, space_character, firstUpowers = False):    #one_string:输入的字符串；space_character:字符串的间隔符，以其做为分隔标志
	if one_string.find(space_character) == -1:
		if not firstUpowers:
			return one_string
		else:
			return firstUpower(one_string)
	string_list = str(one_string).split(space_character)    #将字符串转化为list
	if not firstUpowers:
		first = string_list[0].lower()
	else:
		first = string_list[0].capitalize()
	# print(first)
	others = string_list[1:] 
	others_capital = [word.capitalize() for word in others]      #str.capitalize():将字符串的首字母转化为大写
	others_capital[0:0] = [first]
	hump_string = ''.join(others_capital)     #将list组合成为字符串，中间无连接符。
	return hump_string
