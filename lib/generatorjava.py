
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#生成文件

from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os
from itertools import groupby
from lib.entity import *
import utils

java_src = '/src/main/java'
resource_src = '/src/main/resources/'

def generate_enum_class(workspace_root, package_name, table):
	package_dir =package_name.replace('.', '/')
	module_name =table.module_name
	api_root_dir = workspace_root + module_name+'/api'
	api_dir = api_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/api/'
	for field in table.fields:
		if field.name in ['type','status']:
			enums = []
			string_list = str(field.note).split(',')
			if len(string_list) > 0:
				for n in string_list:
					# if  len(n) >0:
					# print(string_list)
					string_list = str(n).split(':')
					if len(string_list) ==2: 
						f = enum(string_list[0],string_list[1])
						if f is not None:
							enums.append(f)
					else:
						print(string_list)

			enum_class_name = table.entity_name+field.name[0].upper() + field.name[1:]
			mapperTemplate = Template(filename='./tl/api/enum.tl')
			buf = StringIO()
			ctx = Context(buf, table=table,module_name=module_name,package_name=package_name,class_name=enum_class_name, enums=enums)
			mapperTemplate.render_context(ctx)
			# print(buf.getvalue())
			dto_dir = api_dir+'enums/'
			if not os.path.exists(dto_dir):
				os.makedirs(dto_dir)
			f = open(dto_dir + enum_class_name+'Enum.java', 'w')
			f.write(buf.getvalue())
			f.close()	

def generate_do(workspace_root, package_name, table):
	package_dir =package_name.replace('.', '/')
	module_name =table.module_name
	service_root_dir = workspace_root + module_name+'/service'
	service = service_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/service/'
	class_name = table.entity_name+'DO'

	mapperTemplate = Template(filename='./tl/service/do.tl')
	buf = StringIO()
	ctx = Context(buf, table=table,module_name=module_name,package_name=package_name,class_name=class_name)
	mapperTemplate.render_context(ctx)
	# print(buf.getvalue())
	entity_dir = service+'entity/'
	if not os.path.exists(entity_dir):
		os.makedirs(entity_dir)
	f = open(entity_dir + class_name+'.java', 'w')
	f.write(buf.getvalue())
	f.close()

	#临时生成一个VO用于Mapper返回值使用
	class_name = table.entity_name+'VO'
	api_root_dir = workspace_root + module_name+'/api'
	api_dir = api_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/api/'
	vo_dir = api_dir+'vo/'
	if not os.path.exists(vo_dir):
		os.makedirs(vo_dir)
	mapperTemplate = Template(filename='./tl/api/tableVO.tl')
	buf = StringIO()
	ctx = Context(buf, table=table,module_name=module_name,package_name=package_name,class_name=class_name)
	mapperTemplate.render_context(ctx)
	f = open(vo_dir + class_name+'.java', 'w')
	f.write(buf.getvalue())
	f.close()

	#table DTO
	if False :
		class_name = table.entity_name+'DTO'
		api_root_dir = workspace_root + module_name+'/api'
		api_dir = api_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/api/'
		vo_dir = api_dir+'dto/'
		if not os.path.exists(vo_dir):
			os.makedirs(vo_dir)
		mapperTemplate = Template(filename='./tl/api/tableDTO.tl')
		buf = StringIO()
		ctx = Context(buf, table=table,module_name=module_name,package_name=package_name,class_name=class_name)
		mapperTemplate.render_context(ctx)
		f = open(vo_dir + class_name+'.java', 'w')
		f.write(buf.getvalue())
		f.close()

def generate_mapper_class(workspace_root, package_name, table):
	package_dir =package_name.replace('.', '/')
	module_name =table.module_name
	service_root_dir = workspace_root + module_name+'/service'
	service = service_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/service/'

	mapperTemplate = Template(filename='./tl/service/mapper.tl')
	buf = StringIO()
	ctx = Context(buf, table=table,module_name=module_name,package_name=package_name)
	mapperTemplate.render_context(ctx)
	# print(buf.getvalue())
	mapper_dir = service+'repository/mapper/'
	if not os.path.exists(mapper_dir):
		os.makedirs(mapper_dir)
	f = open(mapper_dir +table.entity_name+'Mapper.java', 'w')
	f.write(buf.getvalue())
	f.close()

def generate_mapper_xml(workspace_root, package_name, table):
	package_dir =package_name.replace('.', '/')
	module_name =table.module_name
	service_root_dir = workspace_root + module_name+'/service'
	service = service_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/service/'
	service_resource = workspace_root + module_name+'/service'+resource_src

	mapperTemplate = Template(filename='./tl/service/mapperXml.tl')
	buf = StringIO()
	ctx = Context(buf, table=table,module_name=module_name,package_name=package_name,class_name=table.entity_name)
	mapperTemplate.render_context(ctx)
	# print(buf.getvalue())
	mapper_dir = service_resource+'/com/'+package_dir+'/'+module_name+'/service/repository/mapper/'
	if not os.path.exists(mapper_dir):
		os.makedirs(mapper_dir)
	f = open(mapper_dir +table.entity_name+'Mapper.xml', 'w')
	f.write(buf.getvalue())
	f.close()


def write_parent(workspace_root, package_name):
	os.system('cp -r ./template/parent '+ workspace_root)
	parent_dir = workspace_root + 'parent/'
	if not os.path.exists(parent_dir):
		os.makedirs(parent_dir)
	mapperTemplate = Template(filename='./tl/pom/parent.tl',input_encoding='utf-8')
	buf = StringIO()
	ctx = Context(buf, package_name=package_name)
	mapperTemplate.render_context(ctx)
	f = open(parent_dir+'pom.xml', 'w')
	f.write(buf.getvalue())
	f.close()

def generate_sql(workspace_root, tables):

	mapperTemplate = Template(filename='./tl/sql.tl',input_encoding='utf-8')
	buf = StringIO()
	ctx = Context(buf, tables=tables)
	mapperTemplate.render_context(ctx)
	f = open(workspace_root+'database.sql', 'a')
	f.write(buf.getvalue())
	f.close()

def write_api(workspace_root, package_name, action):
	package_dir =package_name.replace('.', '/')
	generate_enum_class_flag = True
	generate_dto_flag = True

	module_name = action.module_name

	api_root_dir = workspace_root + module_name+'/api'
	api_dir = api_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/api/'

	mapperTemplate = Template(filename='./tl/pom/api.tl',input_encoding='utf-8')
	buf = StringIO()
	ctx = Context(buf, package_name=package_name, module_name=module_name)
	mapperTemplate.render_context(ctx)
	f = open(api_root_dir+'/pom.xml', 'w')
	f.write(buf.getvalue())
	f.close()

	dto_dir = api_dir+'dto/'
	if not os.path.exists(dto_dir):
		os.makedirs(dto_dir)
	vo_dir = api_dir+'vo/'
	if not os.path.exists(vo_dir):
		os.makedirs(vo_dir)

	# if generate_enum_class_flag :
		# generate_enum_class(class_name,class_comment,fields,module_name,table_name,package_name,api_dir)

	if generate_dto_flag :
		if action.has_request() :
			mapperTemplate = Template(filename='./tl/api/dto.tl')
			buf = StringIO()
			ctx = Context(buf, package_name=package_name, action=action)
			mapperTemplate.render_context(ctx)
			# print(buf.getvalue())
			f = open(dto_dir + action.class_name+'DTO.java', 'w')
			f.write(buf.getvalue())
			f.close()
		if action.has_response() :
			mapperTemplate = Template(filename='./tl/api/vo.tl')
			buf = StringIO()
			ctx = Context(buf, package_name=package_name, action=action)
			mapperTemplate.render_context(ctx)
			# print(buf.getvalue())
			f = open(vo_dir + action.class_name+'VO.java', 'w')
			f.write(buf.getvalue())
			f.close()

def write_controllers(workspace_root, package_name, actions):
	package_dir =package_name.replace('.', '/')
	# print(actions)
	for root_path, g in groupby(actions,key=lambda x:x.get_root_path()):
		acs = list(g)
		module_name = acs[0].module_name

		admin_contoller_root = workspace_root + module_name+'/admin-controller'
		admin_contoller = admin_contoller_root +java_src+'/com/'+package_dir+'/'+module_name+'/'

		mapperTemplate = Template(filename='./tl/pom/admin.tl',input_encoding='utf-8')
		buf = StringIO()
		ctx = Context(buf, package_name=package_name, module_name=module_name)
		mapperTemplate.render_context(ctx)
		f = open(admin_contoller_root+'/pom.xml', 'w')
		f.write(buf.getvalue())
		f.close()

		if root_path.startswith('/op') :
			mapperTemplate = Template(filename='./tl/controller/adminController.tl')
			buf = StringIO()
			ctx = Context(buf, actions=acs, package_name=package_name, module_name=module_name)
			mapperTemplate.render_context(ctx)
			# print(buf.getvalue())
			service_dir = admin_contoller+'controller/'
			if not os.path.exists(service_dir):
				os.makedirs(service_dir)
			f = open(service_dir + 'Admin'+utils.firstUpower(module_name)+'Controller.java', 'w')
			f.write(buf.getvalue())
			f.close()

		controller_root = workspace_root + module_name+'/controller'
		controller = controller_root +java_src+'/com/'+package_name+'/'+module_name+'/'
		mapperTemplate = Template(filename='./tl/pom/controller.tl',input_encoding='utf-8')
		buf = StringIO()
		ctx = Context(buf, package_name=package_name, module_name=module_name)
		mapperTemplate.render_context(ctx)
		f = open(controller_root+'/pom.xml', 'w')
		f.write(buf.getvalue())
		f.close()

		if not root_path.startswith('/op') :
			mapperTemplate = Template(filename='./tl/controller/controller.tl')
			buf = StringIO()
			ctx = Context(buf, actions=acs, package_name=package_name, module_name=module_name)
			mapperTemplate.render_context(ctx)
			# print(buf.getvalue())
			service_dir = controller+'controller/'
			if not os.path.exists(service_dir):
				os.makedirs(service_dir)
			f = open(service_dir + utils.firstUpower(module_name)+'Controller.java', 'w')
			f.write(buf.getvalue())
			f.close()

def write_services(workspace_root, package_name, actions):
	package_dir =package_name.replace('.', '/')
	for module_name, g in groupby(actions,key=lambda x:x.module_name):
		acs = list(g)

		service_root_dir = workspace_root + module_name+'/service'
		service = service_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/service/'
		service_resource = workspace_root + module_name+'/service'+resource_src
		service_dir = service + 'service/'
		service_impl_dir = service + 'service/impl/'

		mapperTemplate = Template(filename='./tl/pom/service.tl',input_encoding='utf-8')
		buf = StringIO()
		ctx = Context(buf, package_name=package_name, module_name=module_name)
		mapperTemplate.render_context(ctx)
		f = open(service_root_dir+'/pom.xml', 'w')
		f.write(buf.getvalue())
		f.close()

		mapperTemplate = Template(filename='./tl/service/commandService.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		if not os.path.exists(service_dir):
			os.makedirs(service_dir)
		f = open(service_dir + utils.firstUpower(module_name)+'CommandService.java', 'w')
		f.write(buf.getvalue())
		f.close()
		mapperTemplate = Template(filename='./tl/service/commandServiceImpl.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		# print(buf.getvalue())
		if not os.path.exists(service_impl_dir):
			os.makedirs(service_impl_dir)
		f = open(service_impl_dir + utils.firstUpower(module_name)+'CommandServiceImpl.java', 'w')
		f.write(buf.getvalue())
		f.close()

		mapperTemplate = Template(filename='./tl/service/queryService.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		# print(buf.getvalue())
		if not os.path.exists(service_dir):
			os.makedirs(service_dir)
		f = open(service_dir + utils.firstUpower(module_name)+'QueryService.java', 'w')
		f.write(buf.getvalue())
		f.close()

		mapperTemplate = Template(filename='./tl/service/queryServiceImpl.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		# print(buf.getvalue())
		if not os.path.exists(service_impl_dir):
			os.makedirs(service_impl_dir)
		f = open(service_impl_dir + utils.firstUpower(module_name)+'QueryServiceImpl.java', 'w')
		f.write(buf.getvalue())
		f.close()

def write_repositories(workspace_root, package_name, actions):
	package_dir =package_name.replace('.', '/')
	for module_name, g in groupby(actions,key=lambda x:x.module_name):
		acs = list(g)

		service_root_dir = workspace_root + module_name+'/service'
		service = service_root_dir+java_src+'/com/'+package_dir+'/'+module_name+'/service/'
		service_resource = workspace_root + module_name+'/service'+resource_src
		service_dir = service + 'service/'

		mapperTemplate = Template(filename='./tl/service/repository.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		# print(buf.getvalue())
		service_dir = service + 'repository/'
		if not os.path.exists(service_dir):
			os.makedirs(service_dir)
		f = open(service_dir + utils.firstUpower(module_name)+'Repository.java', 'w')
		f.write(buf.getvalue())
		f.close()

		mapperTemplate = Template(filename='./tl/service/repositoryImpl.tl')
		buf = StringIO()
		ctx = Context(buf,actions=actions, module_name=module_name, package_name=package_name)
		mapperTemplate.render_context(ctx)
		# print(buf.getvalue())
		service_dir = service+'repository/impl/'
		if not os.path.exists(service_dir):
			os.makedirs(service_dir)
		f = open(service_dir +  utils.firstUpower(module_name) +'RepositoryImpl.java', 'w')
		f.write(buf.getvalue())
		f.close()


def write_module(workspace_root, package_name, module_name):
	if (len(module_name) == 0):
		return
	if not os.path.exists(workspace_root + module_name):
		os.makedirs(workspace_root + module_name)
	os.system('cp -r ./template/module/* '+ workspace_root + module_name)

	package_name = package_name.replace('.', '/')

	mapperTemplate = Template(filename='./tl/pom/module.tl',input_encoding='utf-8')
	buf = StringIO()
	ctx = Context(buf, package_name=package_name, module_name=module_name)
	mapperTemplate.render_context(ctx)
	f = open(workspace_root + module_name+'/pom.xml', 'w')
	f.write(buf.getvalue())
	f.close()

	admin_contoller = workspace_root + module_name+'/admin-controller'+java_src+'/com/'+package_name+'/'+module_name+'/admin/'


def write_projects(workspace_root, package_name, tables,actions):
	write_parent(workspace_root,package_name )
	generate_sql(workspace_root,tables)
	for t in tables:
		write_module(workspace_root, package_name, t.module_name)
		generate_do(workspace_root, package_name,t)
		generate_mapper_class(workspace_root, package_name,t)
		generate_mapper_xml(workspace_root, package_name,t)
		generate_enum_class(workspace_root, package_name,t)
	for x in actions:
		write_module(workspace_root, package_name, x.module_name)
		write_api(workspace_root, package_name,x)
	write_controllers(workspace_root, package_name,actions)
	write_services(workspace_root, package_name,actions)
	write_repositories(workspace_root, package_name,actions)

def write_project(workspace_root, package_name, table, action):
	write_module(workspace_root, package_name, action.module_name)
	write_module(workspace_root, package_name, table.module_name)
	write_api(workspace_root, package_name,action)

	
