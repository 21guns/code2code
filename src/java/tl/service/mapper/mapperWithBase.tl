package com.${package_name}.${module_name}.service.repository.mapper;

import com.guns21.mybatis.mapper.BaseMapper;

import com.${package_name}.${module_name}.service.entity.${class_name}DO;
import com.${package_name}.${module_name}.api.dto.${class_name}DTO;
import com.${package_name}.${module_name}.api.dto.query.${class_name}Query;

public interface ${class_name}Mapper extends BaseMapper<${class_name}DTO, ${class_name}Query, ${class_name}DO> {

}