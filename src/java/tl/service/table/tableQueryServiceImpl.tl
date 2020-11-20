package ${java_class.package};
<%
    class_name =java_class.original_class_name
    id_field = java_class.id_field
%>
import java.util.List;
import java.util.Optional;
import java.util.Objects;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import com.guns21.data.domain.result.PageData;
import com.guns21.common.util.ObjectUtils;
import ${java_class.module_package}.api.dto.${class_name}DTO;
import ${java_class.module_package}.api.dto.query.${class_name}Query;
import ${java_class.module_package}.service.entity.${class_name}DO;
import ${java_class.module_package}.service.query.${class_name}QueryService;
import ${java_class.module_package}.service.repository.mapper.${class_name}Mapper;

/**
 * @author jliu
 * @date
 */
@Service
@Slf4j
public class ${java_class.class_name} implements ${class_name}QueryService {

    @Autowired
	private ${class_name}Mapper mapper;

    @Override
    public List<${class_name}DTO> page(${class_name}DTO query, PageData pagerParams) {
    	return mapper.pageList(query, pagerParams.getPage(), pagerParams.getSize());
    }
    % if id_field is not None :
    @Override
    public Optional<${class_name}DTO> getById(${id_field.type} id) {
        % if id_field.type == "String" :
        if (ObjectUtils.hasText(id)) {
        % elif id_field.type == "Long":
        if (Objects.nonNull(id)) {
        % endif
            return mapper.selectById(id);
        }
        return Optional.empty();
    }
    % endif


}