package com.${package_name}.${module_name}.service.service;
<%!
	import utils
%>
import com.guns21.data.domain.result.MessageResult;
% for a in actions:
	% if a.has_request() and not a.is_get_method():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
	% endif
% endfor

public interface ${utils.firstUpower(module_name)}CommandService {
	% for a in actions:
		% if not a.is_get_method() :
		
	/**
 	 * ${a.comment}
	 */
    MessageResult ${a.get_method_name()}(${a.get_service_method_params()});
    	% endif 
	% endfor

}