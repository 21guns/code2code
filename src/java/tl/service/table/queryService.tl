package ${java_class.package};
<%
    class_name =java_class.original_class_name
    id_field = java_class.id_field
%>
import java.util.List;
import java.util.Optional;

import com.guns21.data.domain.result.PageData;

import ${java_class.module_package}.api.dto.${class_name}DTO;
import ${java_class.module_package}.api.vo.${class_name}VO;

public interface ${java_class.class_name} {

    List<${class_name}VO> page(${class_name}DTO query, PageData pagerParams);

    % if id_field is not None :
    Optional<${class_name}VO> getById(${id_field.type} id);

    List<${class_name}VO> getByIds(List<${id_field.type}> ids);
    % endif
}