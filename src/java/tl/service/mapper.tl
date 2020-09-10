package com.${package_name}.${module_name}.service.repository.mapper;
<%
    hasId = True
    class_name =table.entity_name
    id_Field =table.get_id_field()
%>
import com.${package_name}.${module_name}.service.entity.${class_name}DO;
import com.${package_name}.${module_name}.api.vo.${class_name}VO;

import java.util.Optional;

public interface ${class_name}Mapper {

    Integer insert(${class_name}DO record);

    Integer insertSelective(${class_name}DO record);

    Integer updateByPrimaryKeySelective(${class_name}DO record);

    Integer updateByPrimaryKey(${class_name}DO record);
    
% if table.has_id() :
    Integer deleteByPrimaryKey(${id_Field.type} ${id_Field.name});

    Optional<${class_name}VO> selectByPrimaryKey(${id_Field.type} ${id_Field.name});

    List<${class_name}VO> page(@Param("query") ${class_name}DTO var1, @Param("pageNum") int pageNum, @Param("pageSize") int pageSize);

% endif

}