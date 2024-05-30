package ${java_class.package};
<%
    has_id = java_class.has_id
    class_name =java_class.original_class_name
    id_field = java_class.id_field
%>
import ${java_class.module_package}.service.entity.${class_name}DO;

import java.util.List;

public interface ${class_name}Repository {

    Integer insert(${class_name}DO data);

    Integer insertSelective(${class_name}DO data);

    Integer insertBatch(List<${class_name}DO> list);

    Integer updateByPrimaryKey(${class_name}DO data);

    Integer updateByPrimaryKeySelective(${class_name}DO data);

% if has_id:
    Integer deleteByPrimaryKey(${id_field.type} ${id_field.name});

% endif
}