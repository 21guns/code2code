
from lib import entity 
import utils

class Java_Class(entity.Action):
	"""docstring for Java_Class"""
	def __init__(self, url, http_method,comment):
		super(Java_Class, self).__init__(url, http_method,comment)

	def get_controller_method_params(self):
		params = ''
		for n in self.get_path_variable_name():
			params += '@PathVariable Long ' + n +', '
		if self.has_request():
			if self.http_method != 'GET':
				params += '@RequestBody '
			params += self.class_name + 'DTO dto'
		if params.endswith(', '):
			params = params[:-2]
		if self.response_type == entity.ACTION_RESPONSE_TYPE['PAGE']:
			params += ', PageData pagination'
		return params
	def get_controller_method_invoke_params(self):
		return self.get_controller_method_params().replace('@PathVariable Long ','')\
			.replace(self.class_name + 'DTO ' , '')\
			.replace('PageData ' , '').replace('@RequestBody ','')
	
	def get_controller_mapping(self):
		mapping = '@' + utils.firstUpower(self.http_method) + 'Mapping'
		url = self.url.replace(self.get_root_path(),'')
		if len(url) > 0:
			mapping += '("'+url+'")'
		return mapping

	def get_service_method_params(self):
		params = ''
		for n in self.get_path_variable_name():
			params += 'Long ' + n +', '
		if self.has_request():
			params += self.class_name + 'DTO dto'
		if params.endswith(', '):
			params = params[:-2]
		if self.response_type == entity.ACTION_RESPONSE_TYPE['PAGE']:
			params += ', PageData pagination'
		return params

	def get_service_method_return_type(self):
		# print(self.response_type)
		if self.response_type == entity.ACTION_RESPONSE_TYPE['LIST']:
			return 'List<' + self.class_name + 'VO>'
		elif self.response_type == entity.ACTION_RESPONSE_TYPE['PAGE']:
			return 'List<' + self.class_name + 'VO>'
		elif self.response_type == entity.ACTION_RESPONSE_TYPE['ENTITY']:
			return 'Optional<' + self.class_name + 'VO>'

def new_java_class(url, http_method,comment):
	return Java_Class(url, http_method,comment)