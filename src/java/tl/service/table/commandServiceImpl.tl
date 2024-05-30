package ${java_class.package};
<%
    has_id = java_class.has_id
    id_field =java_class.id_field
    class_name =java_class.original_class_name
%>
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.assembler.AssemblerFactory;
import ${java_class.module_package}.api.dto.${class_name}DTO;
import ${java_class.module_package}.service.entity.${class_name}DO;
import ${java_class.module_package}.service.command.${class_name}CommandService;
import ${java_class.module_package}.service.repository.${class_name}Repository;

import java.util.Optional;
import java.util.List

@Service
@Slf4j
public class ${java_class.class_name} implements ${class_name}CommandService {

 	@Autowired
	private ${class_name}Repository repository;

	@Override
	public MessageResult insert(${class_name}DTO dto) {
	    return Optional.ofNullable(dto)
	    .map(entity -> {
			repository.insert(${class_name}DO.from(entity));
			return MessageResult.success();
		}).orElse(MessageResult.fail());
	}

	@Override
	public MessageResult insertBatch(List<${class_name}DO> dtos) {
		return Optional.ofNullable(dtos)
	    .map(entities -> {
			repository.insertBatch(dtos);
			return MessageResult.success();
		}).orElse(MessageResult.fail());
	}

	@Override
	public MessageResult updateByPrimaryKey(${class_name}DTO dto) {
		return Optional.ofNullable(dto)
	    .map(entity -> {
			repository.updateByPrimaryKey(${class_name}DO.from(entity));
			return MessageResult.success();
		}).orElse(MessageResult.fail());
	}
    % if has_id:
	@Override
	public MessageResult deleteByPrimaryKey(${id_field.type} ${id_field.name}) {
		repository.deleteByPrimaryKey(id);
		return MessageResult.success();
	}
	% endif
}