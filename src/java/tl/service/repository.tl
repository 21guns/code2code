package com.${package_name}.${module_name}.service.repository;
<%!
	import utils
%>
% for a in actions:
	% if a.has_request() and not a.is_get_method():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
	% endif
% endfor

public interface ${utils.firstUpower(module_name)}Repository {

	% for a in actions:
		% if not a.is_get_method() :
		
	/**
 	 * ${a.comment}
	 */
    Integer  ${a.get_method_name()}(${a.get_service_method_params()});
    	% endif 
	% endfor

}