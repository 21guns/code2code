package com.${package_name}.${module_name}.service.service;
<%!
    import utils
%>
import java.util.List;
import java.util.Optional;

import com.guns21.data.domain.result.MessageResult;
import com.guns21.data.domain.result.PageData;
% for a in actions:
	% if a.is_get_method():
		% if a.has_request():
import com.${package_name}.${module_name}.api.dto.${a.class_name}DTO;
		% endif
		% if a.has_response():
import com.${package_name}.${module_name}.api.vo.${a.class_name}VO;
		% endif
	% endif
% endfor

public interface ${utils.firstUpower(module_name)}QueryService {
	% for a in actions:
		% if a.is_get_method() :
		
	/**
 	 * ${a.comment}
	 */
    ${a.get_service_method_return_type()} ${a.get_method_name()}(${a.get_service_method_params()}) ;
    	% endif 
	% endfor

}