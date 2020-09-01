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

/**
 * 
 */
@RestController
##@RequestMapping("/op/v1/${module_name}")
@Slf4j
public class ${utils.firstUpower(module_name)}Controller {

	% for a in actions:
	<%
		params_type = a.class_name + 'DTO dto'
		method_name = a.get_method_name()
		if not a.has_request():
			params_type = ''
		if a.is_get_id_method():
			params_type = '@PathVariable String id'
			method_name = 'get'
	%>
	/**
 	 * ${a.comment}
	 */
	@${utils.firstUpower(a.http_method)}Mapping("${a.url}")
    public MessageResult ${method_name}(${params_type}) {
    	return MessageResult.success();
	} 
	% endfor

}