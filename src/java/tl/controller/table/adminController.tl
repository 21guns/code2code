package ${java_class.package};
<%
	has_id = java_class.has_id
	id_field =java_class.id_field
	class_name =java_class.original_class_name
%>
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import lombok.extern.slf4j.Slf4j;

import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.domain.result.PageData;
import com.guns21.common.util.ObjectUtils;

import ${java_class.module_package}.api.dto.${class_name}DTO;
import ${java_class.module_package}.service.command.${class_name}CommandService;
import ${java_class.module_package}.service.query.${class_name}QueryService;

/**
 * 
 */
@RestController
@Slf4j
@RequestMapping("/op/v1/${java_class.module_name}/${java_class.metadata_name.replace('_', '-')}")
public class ${java_class.class_name} {
    @Autowired
	private ${class_name}QueryService queryService;

    @Autowired
	private ${class_name}CommandService commandService;

	@GetMapping("/{id}")
    public MessageResult<${class_name}DTO> get(@PathVariable Long id) {

		return MessageResult.success(queryService.getById(id).orElse(null));
	} 

	@GetMapping
    public MessageResult page(${class_name}DTO dto, PageData pagerParams) {

		return MessageResult.successPage(queryService.page(dto, pagerParams));   
	} 

	@PostMapping
    public MessageResult save(@RequestBody ${class_name}DTO dto) {
    	return commandService.insert(dto);
	} 

	@PostMapping("/{id}")
    public MessageResult update(@PathVariable String id, @RequestBody ${class_name}DTO dto) {
		if (ObjectUtils.hasText(id)) {
            return commandService.updateByPrimaryKey(dto);
        }
  		return MessageResult.success();
	} 

}