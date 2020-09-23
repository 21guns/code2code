package ${java_class.package}.repository.mapper;
<%
    hasId = java_class.has_id
    id_Field =java_class.id_field
    class_name =java_class.class_name
%>
import ${java_class.project_package}.entity.${class_name}DO;

import java.util.Optional;

public interface ${class_name} {

    Integer insert(${class_name}DO record);

    Integer insertSelective(${class_name}DO record);

    Integer updateByPrimaryKeySelective(${class_name}DO record);

    Integer updateByPrimaryKey(${class_name}DO record);
    
% if has_id:
    Integer deleteByPrimaryKey(${id_Field.type} ${id_Field.name});

    Optional<${class_name}VO> selectByPrimaryKey(${id_Field.type} ${id_Field.name});

    List<${class_name}VO> page(@Param("query") ${class_name}DTO var1, @Param("pageNum") int pageNum, @Param("pageSize") int pageSize);

% endif

}