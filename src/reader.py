from .metadata import metadata, action_metadata, table_metadata
from . import context
from enum import Enum
import re
from itertools import groupby
import xlrd


def read_table(line, space_character):
	str = line.lstrip().rstrip().split(space_character)
	if (len(str) > 2):
		# print(str)
		return 	table_metadata.new_table(str[len(str)-1],str[0])
	if (len(str) < 2):
		print('read_table table line %s' % (str))
	return table_metadata.new_table(str[1],str[0])
	

def del_space(str,space_character):
	"""根据分隔符，拆分字符，将拆分后的字符数组去掉空格

	Args:
		str: | 字段      | 类型    | 描述                  |

	"""
	s = str.lstrip().rstrip().split(space_character)
	ss = list(map(lambda s: s.lstrip().rstrip().replace('`', ''), s))
	return ss

def new_module(str, modules):
	"""
	Args:
		str: ## 机构接口 institutions

	"""
	s = del_space(str, ' ')
	current_module = metadata.Module(s[-1])
	if modules.get(current_module.name) is not None:
		current_module = modules[current_module.name]
	else :
		modules[current_module.name] = current_module
	return current_module


class Reader(object):
    def __init__(self, engine):
        self._engine = engine

    def reader(self, context = context.Context()):
        pass

class MdReader(Reader):
    def __init__(self, engine):
        super(MdReader, self).__init__(engine)

    #str值为|      | ID                | `id`           | `BIGINT(19)`   | Y    | N        | Y        |        |                                                   |
    @staticmethod
    def read_field(str,space_character):
        if str.count('-') > 0:
            return None
        chinese_name_index, name_index = 2, 3
        type_index, pk_index, nullable_index = 4, 5, 6
        unique_index, default_value_index, note_index = 7, 8, 9
        ss = del_space(str, space_character)
        if len(re.findall('[\u4e00-\u9fa5]',ss[name_index])) > 0 :#检查是否包含汉字
            return None
        f = table_metadata.new_field(ss[name_index], ss[chinese_name_index], ss[type_index])
        return f.pk(ss[pk_index] == 'Y').nullable(ss[nullable_index] == 'Y')\
                .unique(ss[unique_index] == 'Y').default_value(ss[default_value_index])\
                .note(ss[note_index])
        
    def reader(self, context = context.Context()):
        modules = {}
        #表结构
        if context.has_table_file :
            current_module = None
            current_table = None
            Table_Phase = Enum('Table_Phase', ('ModuleName', 'Name', 'Field'))
            with open(context.table_file, 'r') as table_file:
                for i, l in enumerate(table_file.readlines()):
                    line = l.strip().lstrip().rstrip() # 把末尾的'\n'删掉
                    if len(line) == 0:
                        continue
                    if re.match('^##\s', line) : # ## 机构 institutions
                        phase = Table_Phase.ModuleName
                        current_module = new_module(line, modules)
                        continue
                    if re.match('^###\s', line) : # ### 邮件模板配置表 email_notification
                        line = line.replace('###','').lstrip().rstrip()
                        if (len(line) == 0):
                            print('\033[1;32;43m table name is None %s \033[0m')
                            continue	
                        current_table = read_table(line, ' ')
                        current_module.add_table(current_table)
                        continue
                    row = re.findall('^\|.*\|',line)
                    if (len(row) == 1):
                        f = self.read_field(line, '|')
                        if current_table != None:
                            current_table.add_fields(f);
                    else:
                        print('\033[1;32;43m table line(%s) = %s \033[0m' % (i, line))

        #接口文档
        if context.has_interface_file :
            current_action = None
            phase = None #接口文档段落
            group = action_metadata.Paramter.DEFAULT_GROUP
            Interface_Phase = Enum('Interface_Phase', ('ModuleName', 'Name', 'Url', 'Method', 'RequestType', 'RequestParamter', 'RequestEg', 'ResponseType', 'ResponseParamter', 'ResponseEg'))
            with open(context.interface_file, 'r') as interfacr_filr:
                for i,l in enumerate(interfacr_filr.readlines()):
                    line = l.strip().lstrip().rstrip() # 把末尾的'\n'删掉
                    if len(line) == 0:
                        continue
                    if re.match('^##\s', line) : # ## 机构接口 institutions
                        phase = Interface_Phase.ModuleName
                        current_module = new_module(line, modules)
                        continue
                    if re.match('^###\s', line) : # 接口中文名称
                        phase = Interface_Phase.Name
                        line = line.replace('###','').lstrip().rstrip()		
                        if (len(line) == 0):
                            print('\033[1;32;43m interface name is None %s \033[0m')
                            continue		
                        current_action = action_metadata.new_action(line, line)
                        current_module.add_action(current_action)
                    if line.startswith('-') or line.startswith('+'):
                        line = line.replace('`', '').lstrip().rstrip()
                        if line.find('接口路径') != -1:#  - 接口路径: `/op/v1/institutions/search`
                            phase = Interface_Phase.Url
                            url = line.split(':')[-1].lstrip().rstrip()
                            if not url.startswith('/') :
                                print('\033[1;32;43m url is error 第%d行 行内容 %s \033[0m' % (i,url))
                                continue
                            current_action.url = url
                            #根据url的第三级目录分析模块英文名称
                            # if modules.get(current_action.module_name()) is not None:
                            # 	current_module = modules[current_action.module_name()]
                            # 	current_module.add_action(current_action)
                            # else :
                            # 	modules[current_action.module_name()] = current_module = metadata.Module(current_action.module_name())
                            # 	current_module.add_action(current_action)

                        if line.find('HTTP Method') != -1:# - HTTP Method: `GET`
                            phase = Interface_Phase.Method
                            current_action.http_method = line.split(':')[-1].lstrip().rstrip()
                    # 		# print(current_action)
                        if line.find('请求参数格式') != -1:#  - 请求参数格式: `QUERY STRING`
                            phase = Interface_Phase.RequestType
                            current_action.request_type = line.split(':')[-1].lstrip().rstrip()

                        if line.find('请求参数') != -1:#  - 请求参数字段
                            phase = Interface_Phase.RequestParamter
                            group = action_metadata.Paramter.DEFAULT_GROUP

                    # 		params_type = True
                    # 		if lines[i+1].find('|') == -1: #无参数
                    # 			pass
                            continue
                        if line.find('请求示例') != -1:#  - 请求示例
                            phase = Interface_Phase.RequestEg
                            # params_type = 'Request
                        if line.find('响应类型') != -1:#  - 响应类型
                            phase = Interface_Phase.ResponseType
                            # print(line.split(':')[-1])
                            current_action.response_type = line.split(':')[-1].lstrip().rstrip()
                    # 		pass

                        if (line.find('响应字段') != -1) or (line.find('响应参数') != -1):#  - 响应字段
                            phase = Interface_Phase.ResponseParamter
                            group = action_metadata.Paramter.DEFAULT_GROUP

                            continue
                        if line.find('响应示例') != -1:#  - 响应字段
                            phase = Interface_Phase.ResponseEg

                    row = re.findall('^\|.*\|',line)
                    if (phase == Interface_Phase.RequestParamter or phase == Interface_Phase.ResponseParamter):
                        if (len(row) == 1):
                            if line.count('-') or line.count('+')> 0:
                                continue
                            if len(re.findall('字段',line)) and  len(re.findall('类型',line)) > 0 :
                                continue
                            parms = del_space(line, '|')
                            # print(parms)
                            if (phase == Interface_Phase.RequestParamter):
                                current_action.add_request_params(parms[1], parms[2], parms[4], group)
                            if (phase == Interface_Phase.ResponseParamter):
                                current_action.add_response_params(parms[1], parms[2], parms[3], group)
                        elif line.startswith('-') or line.startswith('+'):
                            # 设置参数group
                            l = line.replace('`', '').lstrip().rstrip().split(' ')
                            group = l[1];

                        else:
                            print('\033[1;32;43m interface line(%s) = %s \033[0m' % (i, line))

        return modules


class ExcelReader(Reader):
    def __init__(self, engine):
        super(ExcelReader, self).__init__(engine)

    @staticmethod
    def read_db_field(worksheet, rown):
        # print(str)

        chinese_name_index, name_index = 2, 3
        type_index, pk_index, nullable_index = 4, 5, 6
        unique_index, default_value_index, note_index = 7, 9, 10
        # print(worksheet.cell_value(rown,2))
        f = table_metadata.new_field(worksheet.cell_value(rown,name_index), worksheet.cell_value(rown,chinese_name_index), worksheet.cell_value(rown,type_index))

        return f.pk(worksheet.cell_value(rown,pk_index) in ['Y',"是"])\
                .nullable(worksheet.cell_value(rown,nullable_index) in ['Y',"是",""])\
                .unique(worksheet.cell_value(rown,unique_index) in ['Y',"是"])\
                .default_value(worksheet.cell_value(rown,default_value_index))\
                .note(worksheet.cell_value(rown,note_index))

    def reader(self, context = context.Context()):
        modules = {}
        #表结构
        if context.has_table_file :
            #打开一个workbook
            workbook = xlrd.open_workbook(context.table_file)
            #抓取所有sheet页的名称
            worksheets = workbook.sheet_names()
            print('worksheets is %s' %worksheets)
            current_module = None
            current_table = None
            for sheet_name in worksheets:
                if sheet_name in ['']:
                    continue
                print(sheet_name)
                module_name = sheet_name
                current_module = new_module(module_name, modules)
                worksheet = workbook.sheet_by_name(sheet_name)
                num_rows = worksheet.nrows
                num_cols = worksheet.ncols
                actions = []

                fields = []
                field_names = []
                table_name = ''
                #遍历sheet1中所有单元格cell
                for rown in range(1, num_rows): 

                    if len(worksheet.cell_value(rown,1)) > 0:
                        fields = []
                        field_names = []
                        # print(worksheet.cell_value(rown,1))
                        current_table = read_table(worksheet.cell_value(rown,1), '\n')
                        current_module.add_table(current_table)
                    # for coln in range(3,4):
                    cell = worksheet.cell_value(rown,3)
                    if len(cell.strip()) <= 0:
                        continue
                    f = self.read_db_field(worksheet,rown)
                    if current_table != None:
                        current_table.add_fields(f)
        # print(modules)
        return modules
        pass