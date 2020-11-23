package ${java_class.package};
<%
    has_id = java_class.has_id
    class_name =java_class.original_class_name
    id_field = java_class.id_field
%>
import ${java_class.module_package}.service.entity.${class_name}DO;

public interface ${class_name}Repository {

    Integer save(${class_name}DO data);

    Integer updateByPrimaryKey(${class_name}DO data);

% if has_id:
    Integer deleteByPrimaryKey(${id_field.type} ${id_field.name});

% endif
}