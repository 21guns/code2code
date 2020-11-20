package ${java_class.package};
<%
    class_name =java_class.original_class_name
%>
import com.guns21.data.domain.result.MessageResult;

import ${java_class.module_package}.api.dto.${class_name}DTO;

public interface ${java_class.class_name} {

	MessageResult save(${class_name}DTO dto);

    MessageResult update(${class_name}DTO dto);

    MessageResult deleteById(String id);

}