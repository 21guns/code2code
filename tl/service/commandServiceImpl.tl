package com.${package_name}.${module_name}.service.service.impl;
<%!
	import utils
%>
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.assembler.AssemblerFactory;
import com.${package_name}.${module_name}.service.service.${utils.firstUpower(module_name)}CommandService;
import com.${package_name}.${module_name}.service.repository.${utils.firstUpower(module_name)}Repository;
% for a in actions:
	% if a.has_request() and not a.is_get_method():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
	% endif
% endfor

import java.util.Optional;

@Service
@Slf4j
public class ${utils.firstUpower(module_name)}CommandServiceImpl implements ${utils.firstUpower(module_name)}CommandService {

	@Autowired
	private ${utils.firstUpower(module_name)}Repository ${module_name}Repository;
	% for a in actions:
		% if not a.is_get_method() :
		
	/**
 	 * ${a.comment}
	 */
    public MessageResult  ${a.get_method_name()}(${a.get_service_method_params()}) {
    	${module_name}Repository.${a.get_method_name()}(${a.get_controller_method_invoke_params()});
    	return MessageResult.success();
	} 
    	% endif 
	% endfor
}