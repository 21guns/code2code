package ${java_class.package};
<%
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

@Service
@Slf4j
public class ${java_class.class_name} implements ${class_name}CommandService {

 	@Autowired
	private ${class_name}Repository repository;

	@Override
	public 	MessageResult save(${class_name}DTO dto) {
	    return AssemblerFactory.toOptional(dto, ${class_name}DO.class)
	    .map(doo -> {
			repository.save(doo);
			return MessageResult.success();
		}).orElse(MessageResult.fail());
	}

	@Override
	public 	MessageResult update(${class_name}DTO dto) {
	    return AssemblerFactory.toOptional(dto, ${class_name}DO.class)
			.map(doo -> {
			repository.update(doo);
			return MessageResult.success();
		}).orElse(MessageResult.fail());
	}

	@Override
	public MessageResult deleteById(String id) {
		repository.deleteById(id);
		return MessageResult.success();
	}
}