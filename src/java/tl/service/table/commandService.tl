package ${java_class.package};
<%
    has_id = java_class.has_id
    id_field =java_class.id_field
    class_name =java_class.original_class_name
%>
import com.guns21.data.domain.result.MessageResult;

import ${java_class.module_package}.api.dto.${class_name}DTO;

public interface ${java_class.class_name} {

	MessageResult save(${class_name}DTO dto);

    MessageResult updateByPrimaryKey(${class_name}DTO dto);

    % if has_id:
    MessageResult deleteByPrimaryKey(${id_field.type} ${id_field.name});
    % endif

}