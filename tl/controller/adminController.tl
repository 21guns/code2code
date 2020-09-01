package com.${package_name}.${module_name}.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import lombok.extern.slf4j.Slf4j;
<%!
	import utils
%>
% for a in actions:
	% if a.has_request():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
	% endif
% endfor
import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.domain.result.PageData;
import com.${package_name}.${module_name}.service.service.${utils.firstUpower(module_name)}QueryService;
import com.${package_name}.${module_name}.service.service.${utils.firstUpower(module_name)}CommandService;
/**
 * 
 */
@RestController
@RequestMapping("${actions[0].get_root_path()}")
@Slf4j
public class Admin${utils.firstUpower(module_name)}Controller {

	@Autowired
	private ${utils.firstUpower(module_name)}QueryService ${module_name}QueryService;

	@Autowired
	private ${utils.firstUpower(module_name)}CommandService ${module_name}CommandService;
	% for a in actions:

	/**
 	 * ${a.comment}
	 */
	${a.get_controller_mapping()}
    public MessageResult ${a.get_method_name()}(${a.get_controller_method_params()}) {
    	% if a.is_get_method():
    	return MessageResult.success(${module_name}QueryService.${a.get_method_name()}(${a.get_controller_method_invoke_params()}));
    	% else:
    	return ${module_name}CommandService.${a.get_method_name()}(${a.get_controller_method_invoke_params()});
    	% endif
	} 
	% endfor

}