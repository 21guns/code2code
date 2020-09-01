import re
import utils

class Field(object):

	def __init__(self, name, jdbcType, type, javaType, databaseType, comment, note, isId):
		self.name = utils.convert(name,'_',False)
		self.comment = comment
		self.field = name
		self.note = note
		self.isId = isId
		self.jdbcType = jdbcType
		self.type = type
		self.javaType = javaType
		self.databaseType = databaseType
		if (self.jdbcType == "INT") :
			self.jdbcType = "INTEGER"
		elif (self.jdbcType == "BIGINT UNSIGNED"):
			self.jdbcType = "BIGINT"
		elif (self.jdbcType == "DATETIME"):
			self.jdbcType = "TIMESTAMP"

	def is_id(self):
		return self.isId

	def __str__(self):
		return 'Field:name=%s field=%s comment=%s isId=%s' % (self.name, self.field, self.comment, self.isId)
	__repr__ = __str__

def read_db_field(name, jdbcType, comment, note, isId):
	databaseType = jdbcType
	jdbcType = jdbcType.split('(')[0]
	type = None
	javaType = None
	if "VARCHAR" in jdbcType:
		type = "String"
		javaType = "java.lang.String"
	elif "TINYINT" in jdbcType:
		type = "Byte"
		javaType = "java.lang.Byte"
	elif "DATETIME" in jdbcType:
		type = "LocalDateTime"
		javaType = "java.time.LocalDateTime"
	elif "DATE" in jdbcType:
		type = "LocalDate"
		javaType = "java.time.LocalDate"
	elif "DECIMAL" in jdbcType:
		type = "BigDecimal"
		javaType = "java.math.BigDecimal"
	elif "INT" == jdbcType:
		type = "Integer"
		javaType = "java.lang.Integer"
	elif "BIGINT UNSIGNED" == jdbcType:
		type = "Long"
		javaType = "java.lang.Long"
	elif "BIGINT" == jdbcType:
		type = "Long"
		javaType = "java.lang.Long"
	elif "JSON" == jdbcType:
		type = "HashMap"
		javaType = "java.util.HashMap"
	else:
		type = None
		print(name, jdbcType)
	if type is not None :
		return Field(name, jdbcType, type, javaType, databaseType, comment, note, isId)
	return None

def read_interface_field(name, type, comment):
	if type.startswith('-'):
		return None
	if type.startswith('List'):
		type = type.replace('List','java.util.List')
	# if not type.isalnum() : # 不是字母
	# 	return None
	if len(re.findall('[\u4e00-\u9fa5]',type)) > 0 :#检查是否包含汉字
		return None
	if type.lower() == 'number':
		type = 'Integer'
	return Field(name, '', type, '', '', comment, '', False)

class Table(object):
	def __init__(self, name, comment):
		self.name = name
		self.comment = comment
		self.entity_name = utils.convert(name,'_',True)
		self.fields = []
		self.module_name = ''
		self.id_field = None

	def set_module_name(self, module_name):
		self.module_name = module_name

	def get_id_field(self):
		return self.id_field

	def has_id(self):
		return not self.id_field is None

	def add_fields(self, field):
		if field is not None :
			if field.is_id():
				self.id_field = field
			self.fields.append(field)

	def __str__(self):
		return 'Student:name=%s entity_name=%s fields=%s' % (self.name, self.entity_name, self.fields)
	__repr__ = __str__

def read_table(line, space_character):
	str = line.lstrip().rstrip().split(space_character)
	if (len(str) > 2):
		# print(str)
		return 	Table(str[len(str)-1],str[0])
	if (len(str) < 2):
		print(str)
	return Table(str[1],str[0])

ACTION_RESPONSE_TYPE = {
	'LIST':'LIST',
	'PAGE':'PAGE',
	'ENTITY':'ENTITY'
}
ACTION_REQUEST_TYPE = {
	'PATH':'PATH',
	'QUERY':'QUERY',
	'JSON':'JSON'
}

class Action(object):
	def __init__(self, url, http_method,comment):
		self.url = url
		self.http_method =http_method
		self.request_params = []
		self.request_type = ACTION_REQUEST_TYPE['QUERY']
		self.response = []
		self.response_type = ACTION_RESPONSE_TYPE['LIST']
		self.comment =comment
		self.module_name = ''
		self.class_name = ''
		self.url_path = None

	def set_url(self,url):
		# print( url.lstrip().rstrip())
		self.url = url.lstrip().rstrip().replace('`', '')
		self.url_path = urlPath(self.url)
		#/op/v1/module_name 
		self.module_name = self.url_path.module_name()

	def get_root_path(self):
		return self.url_path.root

	def set_http_method(self,http_method):
		# print( http_method.lstrip().rstrip())
		self.http_method = http_method.lstrip().rstrip().replace('`', '')
		self.class_name = self.get_method_name()#utils.firstUpower(self.http_method) + utils.firstUpower(self.url_path.last_path_name())
		self.class_name = self.class_name[0].capitalize() + self.class_name[1:]

	def set_module_name(self, module_name):
		self.module_name = module_name

	def check(self):
		if not self.url.startswith('/') :
			return False
		if self.http_method not in ['POST','GET','PUT','DELETE']:
			return False
		return True

	def is_get_method(self):
		return self.http_method in ['GET']

	def add_request_params(self,field):
		if field is not None :
			self.request_params.append(field)

	def set_request_type(self, type):
		self.request_type = type.lstrip().rstrip().replace('`', '')

	def add_response_params(self,field):
		if field is not None :
			self.response.append(field)

	def set_response_type(self, type):
		self.response_type = type.lstrip().rstrip().replace('`', '')

	def is_get_id_method(self):
		#get /ddd/{id}
		lastUrl = self.url_path.last_path()
		if lastUrl.startswith('{') and self.http_method == 'GET':
			if len(self.request_params) <= 1 :
				# print(self.http_method,self.url,self.request_params)
				return True
	def get_method_name(self):
		method_name = self.url_path.last_path_name()
		if method_name in ['id','no']:
			method_name = self.url_path.after_module_name() + "By" + utils.firstUpower(method_name)
		else:
			method_name = self.url_path.after_module_name()

		return self.http_method.lower() + method_name

	def has_request(self):
		if self.is_get_id_method() :
			return False
		return len(self.request_params) >0 

	def has_response(self):
		return len(self.response) >0 

	def has_path_variable(self):
		return len(self.url_path.path_variable_index)>0

	def get_path_variable_name(self):
		return self.url_path.path_variable_name

	def __str__(self):
		return '%s:%s request_params=%s response=%s root_path=%s' % ( self.http_method,self.url, self.request_params, self.response,self.get_root_path())
	__repr__ = __str__

#/op/v1/module_name/xx/xx
class urlPath(object):
	def __init__(self, url):
		self.url = url
		self.path = self.url.lstrip().rstrip().split('/')
		self.root = '/'.join(self.path[0:4])
		self.path_variable_name = []
		self.path_variable_index = []
		self.path_not_variable = []
		for i,p in enumerate(self.path):
			if p.startswith('{'):
				self.path_variable_name.append(p.replace('{','').replace('}',''))
				self.path_variable_index.append(i)
			else:
				self.path_not_variable.append(p)

	def module_name(self):
		return self.path[3]

	def last_path(self):
		return self.path[-1]

	def last_path_name(self):
		if (self.last_path().startswith('{')):
			return self.path_variable_name[-1]
		else :
			return self.last_path()

	def path_name(self, begin, step):
		return ''.join(map(utils.firstUpower, self.path_not_variable[begin:step]))

	def after_module_name(self):
		return self.path_name(4, len(self.path))

	def __str__(self):
		return '%s:%s request_params=%s response=%s' % ( self.http_method,self.url, self.request_params, self.response)
	__repr__ = __str__

class enum(object):
	def __init__(self, name,comment):
		self.name = name.lstrip().rstrip()
		self.comment = comment.lstrip().rstrip()